# Generated by Django 4.2.5 on 2023-10-24 14:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='reservationrow',
            old_name='number',
            new_name='quantity',
        ),
    ]
