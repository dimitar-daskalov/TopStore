from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from TopStore.products.models import Product, Like

UserModel = get_user_model()


class LikeProductTests(TestCase):
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
        self.like = Like.objects.create(
            product=self.product,
            user=self.user_not_staff,
        )

    def test_LikeProductWhenAuthenticatedUserIsNotStaff_expectToBeSuccessfulAndRedirect(self):
        self.client.force_login(self.user_not_staff)
        response = self.client.get(reverse('like product', kwargs={'pk': self.product.id}))
        self.assertEqual(302, response.status_code)

    def test_LikeProductWhenAuthenticatedUserNotStaffAndHaveNotLikedTheProduct_expectToBeSuccessfullyLiked(self):
        self.client.force_login(self.user_not_staff)
        self.assertTrue(self.like)

    def test_LikeProductWhenAuthenticatedUserNotStaffAndHaveLikedTheProduct_expectToBeSuccessfullyDisliked(self):
        self.client.force_login(self.user_not_staff)
        response = self.client.post(reverse('like product', kwargs={'pk': self.product.id}))
        self.assertNotEqual(self.like, self.product.like_set.filter(user_id=self.user_not_staff.id).first())
        self.assertEqual(302, response.status_code)

    def test_LikeProductWhenAuthenticatedUserIsStaff_expectToRedirect(self):
        self.client.force_login(self.user_staff)
        response = self.client.get(reverse('like product', kwargs={'pk': self.product.id}))
        self.assertEqual(302, response.status_code)

    def test_LikeProductWhenAuthenticatedUserIsNotStaffAndPkIsIncorrect_expectHTTP404(self):
        self.client.force_login(self.user_not_staff)
        response = self.client.get(reverse('like product', kwargs={'pk': self.product.id + 1}))
        self.assertEqual(404, response.status_code)

    def test_LikeProductWhenNotAuthenticatedUser_expectToRedirect(self):
        response = self.client.get(reverse('like product', kwargs={'pk': self.product.id}))
        self.assertEqual(302, response.status_code)
