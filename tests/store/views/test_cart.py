from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from TopStore.store.models import Order

UserModel = get_user_model()


class CartTests(TestCase):
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

    def test_CartTemplate_expectToBeCorrect(self):
        self.client.force_login(self.user_not_staff)
        response = self.client.get(reverse('cart'))
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'store/cart.html')

    def test_CartWhenAuthenticatedUserIsNotStaff_expectToBeSuccessful(self):
        self.client.force_login(self.user_not_staff)
        response = self.client.get(reverse('cart'))
        self.assertEqual(200, response.status_code)

    def test_CartWhenAuthenticatedUserIsStaff_expectToBeSuccessful(self):
        self.client.force_login(self.user_staff)
        response = self.client.get(reverse('cart'))
        self.assertEqual(200, response.status_code)

    def test_CartWhenNotAuthenticatedUser_expectToRedirect(self):
        response = self.client.post(reverse('cart'))
        self.assertEqual(302, response.status_code)

    def test_CartWhenAuthenticatedUser_expectToCreateOrGetIncompleteOrder(self):
        self.client.force_login(self.user_not_staff)
        response = self.client.get(reverse('cart'))
        order = Order.objects.get_or_create(
            is_completed=False,
            user=self.user_not_staff,
        )
        self.assertEqual(order[0], Order.objects.filter(user=self.user_not_staff, is_completed=False)[0])
        self.assertEqual(200, response.status_code)
