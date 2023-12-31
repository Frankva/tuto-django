from django.shortcuts import render, redirect
from .models import Product, ReservationRow, Reservation, Category
from django.http import HttpResponse
from functools import reduce, singledispatch
from .forms import ResevationForm
import sys

def set_url_image(product):
    try:
        product['image'] =  product['image'][11:] 
    except TypeError as e:
        print(type(e), e, file=sys.stderr)
        product.image =  product.image.name[11:] 
    return product


def show_products(request, category=None):
    try:
        products= get_products(int(category))
    except Exception as _:
        products = get_products(category)
    context = dict()
    context['categories'] = Category.objects.all().values('name')
    context['products'] = list(map(set_url_image, products))
    context['basketQuantity'] = get_basket(request)
    context['category_now'] = category
    return render(request, 'shop/index.html', context)

@singledispatch
def get_products(category: None):
    return Product.objects.all().values()

@get_products.register
def _(category: str):
    return Product.objects.filter(category__name=category).values()

@get_products.register
def _(category: int):
    return Product.objects.filter(category__id=category).values()


def get_basket(request):
    try:
        basket = request.session['basket']
        return len(basket)
    except KeyError as e:
        print(type(e), e, file=sys.stderr)
    return 0

def images(request, name):
    context = dict()
    context['src'] = 'shop/images/' + name
    return render(request, 'shop/images.html', context)

def add_basket(request, id):
    try:
        return_text = ''
        basket = request.session['basket']
        return_text += str(request.session['basket'])
        basket.append(id)
        return_text += str(request.session['basket'])
        request.session['basket'] = basket
        return redirect('shop:index')
    except (KeyError, AttributeError) as e:
        print(type(e), e, file=sys.stderr)
        request.session['basket'] = list()
        return add_basket(request, id)


def get_data_for_show_basket(id):
    try:
        return Product.objects.get(id=id)
    except Exception as e:
        print(type(e), e, file=sys.stderr)

def get_basket_with_url(basket):
    basket_data = tuple(map(get_data_for_show_basket, basket))
    basket_data_noneless = tuple(filter(lambda product: product is not None,
                                       basket_data))
    basket_with_url = tuple(map(set_url_image, basket_data_noneless))
    return basket_with_url

def get_total_price(basket):
    def sum_price(accumulator, product):
        return accumulator + product.price
    total_price = reduce(sum_price, basket, 0)
    return total_price

def get_basket_from_session(request):
    try:
        basket = request.session['basket']
    except (KeyError, AttributeError) as e:
        print(type(e), e, file=sys.stderr)
        request.session['basket'] = list()
        basket = request.session['basket']
    return basket

def show_basket(request):
    basket = get_basket_from_session(request)
    basket_with_url = get_basket_with_url(basket)
    context = dict()
    context['basket'] = basket_with_url
    context['total_price'] = get_total_price(basket_with_url)
    return render(request, 'shop/basket.html', context)
    
def delete_basket(request):
    request.session['basket'] = list()
    return redirect('shop:show-basket')

def delete_item_basket(request, id):
    try:
        basket = request.session['basket']
        basket.remove(id)
        request.session['basket'] = basket
    except ValueError as e:
        print(type(e), e, file=sys.stderr)
    return redirect('shop:show-basket')

def reservation_form(request):
    context = dict()
    context['form'] = ResevationForm();
    return render(request, 'shop/reservation-form.html', context)

def post_reservation_form(request):
    try:
        context = dict()
        reservation = Reservation.objects.create(date=request.POST['datetime'],
                           first_name=request.POST['first_name'],
                           last_name=request.POST['last_name'],
                           phone_number=request.POST['phone_number'])
        basket = request.session['basket']
        formated_basket = get_quantity_each_item(basket)
        for row in formated_basket:
            product = Product.objects.get(id=row['id'])
            ReservationRow.objects.create(quantity=row['quantity'], reduction=0,
                                  product=product, reservation=reservation)
        request.session['basket'] = list()
        return render(request, 'shop/summary.html', context)
    except Exception as e:
        print(type(e), e, file=sys.stderr)

    

def get_quantity_each_item(basket: list[int]):
    def get_quantity_and_id(item: int):
        row = dict()
        row['quantity'] =basket.count(item)
        row['id'] = item
        return row
    count_basket = tuple(map(get_quantity_and_id, basket))
    def remove_duplicate(acc, item):
        if item not in acc:
            acc.append(item)
        return acc
    duplicateless_count_basket = reduce(remove_duplicate, count_basket, list())
    return duplicateless_count_basket


def get_invoice(request, id):
    context = dict()
    reservation = Reservation.objects.get(id=id)
    reservation_rows = reservation.reservationrow_set.all()
    def format_reservation(row):
        data = dict()
        data['image'] = row.product.image.name[11:]
        data['name'] = row.product.name
        data['description'] = row.product.description
        data['quantity'] = row.quantity
        data['unit_price'] = row.product.price
        data['amount'] = data['quantity'] * data['unit_price']
        return data
    formated_reservation = tuple(map(format_reservation, reservation_rows))
    context['formated_reservation'] = formated_reservation
    context['reservation'] = reservation
    context['total_price'] = reduce(lambda acc, row: acc + row['amount'],
                            formated_reservation, 0)
    return render(request, 'shop/invoice.html', context)
