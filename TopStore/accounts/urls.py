from django.urls import path

from TopStore.accounts.views import sing_in_user, sing_out_user, sing_up_user, details_profile_user, \
    completed_orders_user

urlpatterns = [
    path('login/', sing_in_user, name='sing in user'),
    path('logout/', sing_out_user, name='sing out user'),
    path('register/', sing_up_user, name='sign up user'),
    path('details/', details_profile_user, name='details account user'),
    path('orders/', completed_orders_user, name='completed orders user'),
]
