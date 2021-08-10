from datetime import datetime
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from TopStore.store.models import Order

UserModel = get_user_model()


class CompletedOrdersUserTests(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user(
            email='test@user.user',
            username='test_user',
            password='test_user',
        )

    def test_CompletedOrdersTemplate_expectToBeCorrect(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('completed orders user'))
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'account/orders_information_user.html')

    def test_CompletedOrdersWhenNotAuthenticatedUser_expectToRedirect(self):
        response = self.client.get(reverse('completed orders user'))
        self.assertEqual(302, response.status_code)

    def test_CompletedOrdersWhenAuthenticatedUser_expectToShowCompletedOrdersSuccessfully(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('completed orders user'))
        order = Order.objects.create(
            date_ordered=datetime.now(),
            is_completed=True,
            user=self.user,
        )
        self.assertEqual(order, Order.objects.filter(user=self.user, is_completed=True)[0])
        self.assertEqual(200, response.status_code)

    def test_DetailsWhenNotAuthenticatedUser_expectToRedirect(self):
        response = self.client.post(reverse('completed orders user'))
        self.assertEqual(302, response.status_code)
