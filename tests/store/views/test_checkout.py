from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from TopStore.store.models import Order

UserModel = get_user_model()


class CheckoutTests(TestCase):
    def setUp(self):
        self.user_staff = UserModel.objects.create_user(
            email='test@user_staff.user',
            username='test_user_staff',
            password='test_user_staff',
            is_staff=True
        )
        self.user_not_staff = UserModel.objects.create_user(
            email='test@user.user',
            username='test_user',
            password='test_user',
            is_staff=False
        )
        self.order = Order.objects.create(
            is_completed=True,
            user=self.user_not_staff,
        )

    def test_CheckoutTemplate_expectToBeCorrect(self):
        self.client.force_login(self.user_not_staff)
        response = self.client.get(reverse('checkout'))
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'store/checkout.html')

    def test_CheckoutWhenAuthenticatedUserIsNotStaff_expectToBeSuccessful(self):
        self.client.force_login(self.user_not_staff)
        response = self.client.get(reverse('checkout'))
        self.assertEqual(200, response.status_code)

    def test_CheckoutWhenAuthenticatedUserIsStaff_expectToBeSuccessful(self):
        self.client.force_login(self.user_staff)
        response = self.client.get(reverse('checkout'))
        self.assertEqual(200, response.status_code)

    def test_CheckoutWhenNotAuthenticatedUser_expectToRedirect(self):
        response = self.client.post(reverse('checkout'))
        self.assertEqual(302, response.status_code)

    def test_CheckoutWhenAuthenticatedUser_expectToCreateAnIncompleteOrder(self):
        self.client.force_login(self.user_not_staff)
        response = self.client.post(reverse('checkout'))
        self.assertTrue(Order.objects.filter(user=self.user_not_staff, is_completed=False))
        self.assertEqual(200, response.status_code)
