# Django_test
Essai du framework Django (Python)

* You need to install python (and pip), a MySQL or MariaDB database
* Django must be installed
```bash
python -m pip install Django
```
* Install Django-compatible MySQL python client
```bash
python -m pip install mysqlclient
```
* Install the debug bar
```bash
python -m pip install django-debug-toolbar
```
* Install Pillow (It is for ImageField)
```bash
python -m pip install pillow
```
* Download the project
```bash
git clone https://github.com/OrifInformatique/Django_test
cd Django_test
```
* Configure your database in mysite/settings.py
* Create your database in MySQL or MariaDB
* Tables must be created via :
```bash
python manage.py migrate
```
Create a admin
```bash
python manage.py createsuperuser
```
* Launch the site
```bash
python manage.py runserver
```
Go on :
http://localhost:8000/admin/ 
and create some products with images
