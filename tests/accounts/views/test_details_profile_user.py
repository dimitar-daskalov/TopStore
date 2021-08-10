from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from TopStore.products.models import Product, Like

UserModel = get_user_model()


class DetailsUserTests(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user(
            email='test@user.user',
            username='test_user',
            password='test_user',
        )
        self.product = Product.objects.create(
            type='Television',
            name='Test Television',
            description='Test Television',
            product_image='Test Television.jpg',
            price=150,
        )

    def test_DetailsTemplate_expectToBeCorrect(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('details account user'))
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'account/profile_user.html')

    def test_DetailsWhenAuthenticatedUser_expectToShowDetailsSuccessfully(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('details account user'))
        self.assertEqual(self.user.profile.profile_image, UserModel.objects.get(pk=self.user.id).profile.profile_image)
        self.assertEqual(200, response.status_code)

    def test_DetailsWhenNotAuthenticatedUser_expectToRedirect(self):
        response = self.client.post(reverse('details account user'))
        self.assertEqual(302, response.status_code)

    def test_DetailsWhenAuthenticatedUser_expectToShowDetailsSuccessfully_ShowLikedProducts(self):
        self.client.force_login(self.user)

        liked_product = Like.objects.create(
            product=self.product,
            user=self.user,
        )
        self.assertEqual(liked_product, Like.objects.filter(user_id=self.user.id)[0])
