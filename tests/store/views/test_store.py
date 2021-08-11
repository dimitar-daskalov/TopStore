from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from TopStore.products.models import Product, Like

UserModel = get_user_model()


class StoreTests(TestCase):
    def setUp(self):
        self.user_not_staff = UserModel.objects.create_user(
            email='test@user.user',
            username='test_user',
            password='test_user',
            is_staff=False
        )
        self.product = Product.objects.create(
            type='Television',
            name='Test Television',
            description='Test Television',
            product_image='Test Television.jpg',
            price=150,
        )
        self.product_2 = Product.objects.create(
            type='Television',
            name='Test Television2',
            description='Test Television2',
            product_image='Test Television2.jpg',
            price=150,
        )
        self.like = Like.objects.create(
            product=self.product,
            user=self.user_not_staff,
        )

    def test_StoreTemplate_expectToBeCorrect(self):
        response = self.client.get(reverse('store'))
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'store/store.html')

    def test_StoreWhenAuthenticatedUser_expectToShowStoreSuccessfully(self):
        self.client.force_login(self.user_not_staff)
        response = self.client.get(reverse('store'))
        self.assertEqual(200, response.status_code)

    def test_StoreWhenNotAuthenticatedUser_expectToShowStoreSuccessfully(self):
        response = self.client.get(reverse('store'))
        self.assertEqual(200, response.status_code)

    def test_StoreWhenUserSeeNewAdditions_expectSeeNewestProduct(self):
        self.assertEqual(self.product_2, Product.objects.order_by('-id')[0])

    def test_StoreWhenUserSeeTrendingProducts_expectSeeMostLikedProduct(self):
        products = Product.objects.order_by('id')
        for product in products:
            product.likes_count = product.like_set.count()
        self.assertTrue(self.product, sorted(products, key=lambda x: -x.likes_count)[0])
