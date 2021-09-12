from django.urls import path

from TopStore.accounts.views import sign_in_user, sign_out_user, sign_up_user, details_profile_user, \
    completed_orders_user, contact_messages_users, contact_message_reply, activate_user_email, \
    custom_password_reset_view, \
    CustomPasswordResetDoneView, CustomPasswordResetConfirmView, CustomPasswordResetCompleteView, \
    CustomPasswordChangeView, CustomPasswordChangeDoneView

urlpatterns = [
    path('login/', sign_in_user, name='sign in user'),
    path('logout/', sign_out_user, name='sign out user'),
    path('register/', sign_up_user, name='sign up user'),
    path('details/', details_profile_user, name='details account user'),
    path('orders/', completed_orders_user, name='completed orders user'),
    path('messages/', contact_messages_users, name='contact messages users'),
    path('messages/reply/<int:pk>', contact_message_reply, name='contact message reply'),
    path('activate/<uidb64>/<token>/', activate_user_email, name='activate email user'),

    # Build in authentication views - Django

    path('password_change/', CustomPasswordChangeView.as_view(), name='password_change'),
    path('password_change_complete/', CustomPasswordChangeDoneView.as_view(), name='password_change_done'),
    path('reset_password/', custom_password_reset_view, name='reset_password'),
    path('reset_password_sent/', CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset_password_complete/', CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
