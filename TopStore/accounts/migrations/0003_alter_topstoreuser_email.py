# Generated by Django 3.2.5 on 2021-08-07 16:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_alter_topstoreuser_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='topstoreuser',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
    ]
