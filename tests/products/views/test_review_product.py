from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from TopStore.products.models import Product, Like, Review

UserModel = get_user_model()


class ReviewProductTests(TestCase):
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

    def test_ReviewProductWhenAuthenticatedUserNotStaff_expectToBeSuccessfulAndRedirect(self):
        self.client.force_login(self.user_not_staff)
        response = self.client.post(reverse('review product', kwargs={'pk': self.product.id}))
        review = Review(
            text='This is a test text.',
            product=self.product,
            user=self.user_not_staff
        )
        self.assertTrue(review)
        self.assertEqual(302, response.status_code)

    def test_ReviewProductWhenAuthenticatedUserIsStaff_expectToRedirect(self):
        self.client.force_login(self.user_staff)
        response = self.client.get(reverse('review product', kwargs={'pk': self.product.id}))
        self.assertEqual(302, response.status_code)

    def test_ReviewProductWhenNotAuthenticatedUser_expectToRedirect(self):
        response = self.client.get(reverse('review product', kwargs={'pk': self.product.id}))
        self.assertEqual(302, response.status_code)
