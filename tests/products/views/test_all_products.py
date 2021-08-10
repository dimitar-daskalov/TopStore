from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

UserModel = get_user_model()


class AllProductsTests(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user(
            email='test@user.user',
            username='test_user',
            password='test_user',
        )

    def test_AllProductsTemplate_expectToBeCorrect(self):
        response = self.client.get(reverse('all products'))
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'product/all_products.html')

    def test_AllProductsWhenAuthenticatedUser_expectToShowDetailsSuccessfully(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('all products'))
        self.assertEqual(200, response.status_code)

    def test_AllProductsWhenNotAuthenticatedUser_expectToShowDetailsSuccessfully(self):
        response = self.client.get(reverse('all products'))
        self.assertEqual(200, response.status_code)
