# Generated by Django 3.2.5 on 2021-07-31 16:23

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0007_rename_data_ordered_order_date_ordered'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderinformation',
            name='telephone_number',
            field=models.CharField(max_length=15, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+999999999999'. Up to 15 digits allowed.", regex='^\\+?1?\\d{9,15}$')]),
        ),
        migrations.AlterField(
            model_name='orderinformation',
            name='zip_code',
            field=models.CharField(max_length=10, validators=[django.core.validators.MinLengthValidator(4), django.core.validators.RegexValidator(message='Invalid Zip code.', regex='^(^[0-9]{4}(?:-[0-9]{4})?$|^$)')]),
        ),
    ]
