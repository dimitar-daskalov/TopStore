from django.urls import path

from TopStore.accounts.views import sign_in_user, sign_out_user, sign_up_user, details_profile_user, \
    completed_orders_user, contact_messages_users, contact_message_reply

urlpatterns = [
    path('login/', sign_in_user, name='sign in user'),
    path('logout/', sign_out_user, name='sign out user'),
    path('register/', sign_up_user, name='sign up user'),
    path('details/', details_profile_user, name='details account user'),
    path('orders/', completed_orders_user, name='completed orders user'),
    path('messages/', contact_messages_users, name='contact messages users'),
    path('messages/reply/<int:pk>', contact_message_reply, name='contact message reply'),
]
