from datetime import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from TopStore.store.models import Order

UserModel = get_user_model()


class SignUpUserTests(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user(
            email='test@user.user',
            username='test_user',
            password='test_user',
        )

    def test_SignUpTemplate_expectToBeCorrect(self):
        response = self.client.get(reverse('sign up user'))
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'account/sign_up_user.html')

    def test_SignUpWhenAuthenticatedUser_expectToRedirect(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('sign up user'))
        self.assertEqual(302, response.status_code)

    def test_SignUpWhenNotAuthenticatedUser_expectToSignUpSuccessfully(self):
        response = self.client.post(reverse('sign up user'))
        self.assertEqual(self.user.email, UserModel.objects.get(pk=self.user.id).email)
        self.assertEqual(200, response.status_code)

    def test_SignUpWhenNotAuthenticatedUserSignUpSuccessfully_expectToCreateProfileSuccessfully(self):
        response = self.client.post(reverse('sign up user'))
        self.assertEqual(self.user.email, UserModel.objects.get(pk=self.user.id).email)
        self.assertEqual(self.user.id, UserModel.objects.get(pk=self.user.id).profile.pk)
        self.assertEqual(200, response.status_code)

    def test_SignUpWhenNotAuthenticatedUserSignUpSuccessfully_expectToCreateOrGetIncompleteOrderAndRedirect(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('sign up user'))
        order = Order.objects.create(
            date_ordered=datetime.now(),
            is_completed=False,
            user=self.user,
        )
        self.assertEqual(order, Order.objects.filter(user=self.user, is_completed=False)[0])
        self.assertEqual(302, response.status_code)
