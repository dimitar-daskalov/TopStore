from django.contrib import admin
from django.contrib.admin import ModelAdmin

from TopStore.store.models import ContactMessage, Order, OrderItem, OrderInformation


# Register your models here.

class ContactMessageAdmin(ModelAdmin):
    list_display = ('name', 'email', 'message', 'answered')
    list_filter = ('email', 'answered')
    readonly_fields = ('name', 'email', 'message')


admin.site.register(ContactMessage, ContactMessageAdmin)


class OrderAdmin(ModelAdmin):
    list_display = ('id', 'user', 'date_ordered', 'is_completed')
    list_filter = ('id', 'date_ordered', 'is_completed')


admin.site.register(Order, OrderAdmin)


class OrderItemAdmin(ModelAdmin):

    def order_id(self, instance):
        return instance.order.id

    def user_email(self, instance):
        return instance.order.user.email

    def date_ordered(self, instance):
        return instance.order.date_ordered

    def product_name(self, instance):
        return instance.product.name

    list_display = (
        'order_id', 'user_email', 'date_ordered', 'product_name', 'quantity', 'total_price_item'
    )
    list_filter = ('order__id',)


admin.site.register(OrderItem, OrderItemAdmin)


class OrderAdminInformation(ModelAdmin):
    def order_id(self, instance):
        return instance.order.id

    def user_email(self, instance):
        return instance.order.user.email

    def date_ordered(self, instance):
        return instance.order.date_ordered

    list_display = (
        'order_id', 'user_email', 'date_ordered', 'address', 'city', 'zip_code', 'telephone_number',
    )
    list_filter = ('order__id',)


admin.site.register(OrderInformation, OrderAdminInformation)
