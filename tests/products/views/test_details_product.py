from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from TopStore.products.models import Product

UserModel = get_user_model()


class DetailsProductTests(TestCase):
    def setUp(self):
        self.user_staff = UserModel.objects.create_user(
            email='test_staff@user.user',
            username='test_staff',
            password='test_staff',
            is_staff=True,
        )
        self.user_not_staff = UserModel.objects.create_user(
            email='test_not_staff@user.user',
            username='test_not_staff',
            password='test_not_staff',
            is_staff=False,
        )
        self.product = Product.objects.create(
            type='Television',
            name='Test Television',
            description='Test Television',
            product_image='Test Television.jpg',
            price=150,
        )

    def test_DetailsProductTemplate_expectToBeCorrect(self):
        self.client.force_login(self.user_not_staff)
        response = self.client.get(reverse('details product', kwargs={'pk': self.product.id}))
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'product/details_product.html')

    def test_DetailsProductWhenAuthenticatedUserIsStaff_expectToBeSuccessful(self):
        self.client.force_login(self.user_staff)
        response = self.client.get(reverse('details product', kwargs={'pk': self.product.id}))
        self.assertEqual(200, response.status_code)

    def test_DetailsProductWhenAuthenticatedUserIsNotStaff_expectToBeSuccessful(self):
        self.client.force_login(self.user_not_staff)
        response = self.client.get(reverse('details product', kwargs={'pk': self.product.id}))
        self.assertEqual(200, response.status_code)

    def test_DetailsProductWhenNotAuthenticatedUser_expectToBeSuccessful(self):
        response = self.client.post(reverse('details product', kwargs={'pk': self.product.id}))
        self.assertEqual(200, response.status_code)

    def test_DetailsProductWhenAuthenticatedUserIsStaffAndPkIsIncorrect_expectHTTP404(self):
        self.client.force_login(self.user_staff)
        response = self.client.get(reverse('details product', kwargs={'pk': self.product.id + 1}))
        self.assertEqual(404, response.status_code)

    def test_DetailsProductWhenAuthenticatedUserNotStaffAndPkIsIncorrect_expectHTTP404(self):
        self.client.force_login(self.user_not_staff)
        response = self.client.get(reverse('details product', kwargs={'pk': self.product.id + 1}))
        self.assertEqual(404, response.status_code)

    def test_DetailsProductWhenNotAuthenticatedUserAndPkIsIncorrect_expectHTTP404(self):
        response = self.client.get(reverse('details product', kwargs={'pk': self.product.id + 1}))
        self.assertEqual(404, response.status_code)
