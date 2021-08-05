from django.contrib import admin
from django.contrib.admin import ModelAdmin

from TopStore.products.models import Product


# Register your models here.

class ProductAdmin(ModelAdmin):
    list_display = ('name', 'price', 'type', 'likes_count',)
    list_filter = ('type',)

    def likes_count(self, obj):
        return obj.like_set.count()


admin.site.register(Product, ProductAdmin)
