from django.urls import path

from TopStore.store.views import store, cart, checkout, about, contact, update_item

urlpatterns = [
    path('', store, name='store'),
    path('cart/', cart, name='cart'),
    path('checkout/', checkout, name='checkout'),
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),
    path('update_item/', update_item, name='update_item'),
]
