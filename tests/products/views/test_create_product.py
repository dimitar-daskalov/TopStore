from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

UserModel = get_user_model()


class CreateProductTests(TestCase):
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

    def test_CreateProductTemplate_expectToBeCorrect(self):
        self.client.force_login(self.user_staff)
        response = self.client.get(reverse('create product'))
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'product/create_product.html')

    def test_CreateProductWhenAuthenticatedUserIsStaff_expectToBeSuccessful(self):
        self.client.force_login(self.user_staff)
        response = self.client.get(reverse('create product'))
        self.assertEqual(200, response.status_code)

    def test_CreateProductWhenAuthenticatedUserIsNotStaff_expectToRedirect(self):
        self.client.force_login(self.user_not_staff)
        response = self.client.get(reverse('create product'))
        self.assertEqual(302, response.status_code)

    def test_CreateProductWhenNotAuthenticatedUser_expectToRedirect(self):
        response = self.client.post(reverse('create product'))
        self.assertEqual(302, response.status_code)
