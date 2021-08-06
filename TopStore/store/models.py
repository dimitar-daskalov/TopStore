from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator, RegexValidator
from django.db import models
from TopStore.products.models import Product

# Create your models here.


UserModel = get_user_model()


class ContactMessage(models.Model):
    name = models.CharField(
        max_length=40,
        validators=[
            MinLengthValidator(2),
        ],
    )
    email = models.EmailField()
    message = models.TextField(
        max_length=250,
        validators=[
            MinLengthValidator(2),
        ],
    )
    answered = models.BooleanField(default=False)

    def __str__(self):
        return f'Send by: {self.email}'


class Order(models.Model):
    date_ordered = models.DateTimeField(auto_now_add=True)
    is_completed = models.BooleanField(default=False)
    user = models.ForeignKey(
        UserModel,
        on_delete=models.SET_NULL,
        null=True,
    )

    def __str__(self):
        return f'Order ID: {self.id} - {self.user}'

    @property
    def total_cart_items_price(self):
        order_items_total_price = sum(item.total_price_item for item in self.orderitem_set.all())
        return order_items_total_price

    @property
    def total_cart_items_count(self):
        order_items_total_count = sum(item.quantity for item in self.orderitem_set.all())
        return order_items_total_count


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True)
    data_added = models.DateTimeField(auto_now_add=True)

    @property
    def total_price_item(self):
        return self.quantity * self.product.price

    def __str__(self):
        return f'{self.product} {self.quantity} {self.total_price_item:.2f}'


class OrderInformation(models.Model):
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(
        UserModel,
        on_delete=models.SET_NULL,
        null=True,
    )
    address = models.CharField(
        max_length=30,
        validators=[
            MinLengthValidator(10),
        ],
    )
    city = models.CharField(
        max_length=20,
        validators=[
            MinLengthValidator(3),
        ],
    )
    zip_code = models.CharField(
        max_length=10,
        validators=[
            MinLengthValidator(4),
            RegexValidator(
                regex=r'^(^[0-9]{4}(?:-[0-9]{4})?$|^$)',
                message='Invalid Zip code.',
            ),
        ],
    )
    telephone_number = models.CharField(
        max_length=15,
        validators=[
            RegexValidator(
                regex=r'^\+?1?\d{9,15}$',
                message="Phone number must be entered in the format: '+999999999999'. Up to 15 digits allowed.",
            ),
        ],
    )
    comment = models.TextField(
        max_length=250,
        validators=[
            MinLengthValidator(5),
        ],
        blank=True,
    )

    def __str__(self):
        return f'{self.address}, {self.city}, {self.zip_code}, {self.telephone_number}'
