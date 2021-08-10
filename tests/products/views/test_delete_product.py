from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from TopStore.products.models import Product

UserModel = get_user_model()


class DeleteProductTests(TestCase):
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

    def test_DeleteProductTemplate_expectToBeCorrect(self):
        self.client.force_login(self.user_staff)
        response = self.client.get(reverse('delete product', kwargs={'pk': self.product.id}))
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'product/delete_product.html')

    def test_getDeleteProductWhenAuthenticatedUserIsStaff_expectToBeSuccessful(self):
        self.client.force_login(self.user_staff)
        response = self.client.get(reverse('delete product', kwargs={'pk': self.product.id}))
        self.assertEqual(200, response.status_code)

    def test_postDeleteProductWhenAuthenticatedUserIsStaff_expectToBeSuccessfulAndRedirect(self):
        self.client.force_login(self.user_staff)
        response = self.client.post(reverse('delete product', kwargs={'pk': self.product.id}))
        self.assertEqual(302, response.status_code)

    def test_DeleteProductWhenAuthenticatedUserIsNotStaff_expectToRedirect(self):
        self.client.force_login(self.user_not_staff)
        response = self.client.get(reverse('delete product', kwargs={'pk': self.product.id}))
        self.assertEqual(302, response.status_code)

    def test_DeleteProductWhenNotAuthenticatedUser_expectToRedirect(self):
        response = self.client.get(reverse('delete product', kwargs={'pk': self.product.id}))
        self.assertEqual(302, response.status_code)

    def test_DeleteProductWhenAuthenticatedUserIsStaffAndPkIsIncorrect_expectHTTP404(self):
        self.client.force_login(self.user_staff)
        response = self.client.get(reverse('delete product', kwargs={'pk': self.product.id + 1}))
        self.assertEqual(404, response.status_code)
