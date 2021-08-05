from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator, MinValueValidator
from django.db import models

# Create your models here.

UserModel = get_user_model()


class Product(models.Model):
    TYPE_CHOICE_PHONE = 'Smartphone'
    TYPE_CHOICE_TV = 'Television'
    TYPE_CHOICE_HEADPHONES = 'Headphones'

    TYPE_CHOICES = (
        (TYPE_CHOICE_PHONE, 'Smartphone'),
        (TYPE_CHOICE_TV, 'Television'),
        (TYPE_CHOICE_HEADPHONES, 'Headphones'),
    )

    type = models.CharField(
        max_length=10,
        choices=TYPE_CHOICES,
    )

    name = models.CharField(
        max_length=30,
        validators=[
            MinLengthValidator(5),
        ],
    )

    description = models.TextField(
        max_length=250,
        validators=[
            MinLengthValidator(20),
        ],
    )

    product_image = models.ImageField(
        upload_to='products',
        blank=True,
    )

    price = models.FloatField(
        validators=[
            MinValueValidator(20),
        ],
    )

    def __str__(self):
        return f'Name: {self.name} - Price: {self.price:.2f} BGN - Type: {self.type}'


class Like(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
    )


class Review(models.Model):
    text = models.TextField(
        max_length=150,
        validators=[
            MinLengthValidator(5),
        ]
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
    )
