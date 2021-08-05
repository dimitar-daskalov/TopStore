from django.urls import path

from TopStore.products.views import create_product, update_product, delete_product, details_product, all_products, \
    filter_products, like_product, review_product

urlpatterns = [
    path('create/', create_product, name='create product'),
    path('update/<int:pk>', update_product, name='update product'),
    path('delete/<int:pk>', delete_product, name='delete product'),
    path('details/<int:pk>', details_product, name='details product'),
    path('like/<int:pk>', like_product, name='like product'),
    path('review/<int:pk>', review_product, name='review product'),
    path('all/', all_products, name='all products'),
    path('filter/<str:product_type>', filter_products, name='filter products'),
]
