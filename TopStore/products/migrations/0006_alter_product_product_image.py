# Generated by Django 3.2.5 on 2021-07-25 10:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_remove_product_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='product_image',
            field=models.ImageField(blank=True, default='generic_product.png', upload_to='products'),
        ),
    ]