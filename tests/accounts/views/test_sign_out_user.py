from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

UserModel = get_user_model()


class SignOutUserTests(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user(
            email='test@user.user',
            username='test_user',
            password='test_user',
        )

    def test_SignOutWhenAuthenticatedUser_expectToSingOutSuccessfullyAndRedirect(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('sign out user'))
        self.assertEqual(302, response.status_code)

    def test_SignOutWhenNotAuthenticatedUser_expectToRedirect(self):
        response = self.client.get(reverse('sign out user'))
        self.assertEqual(302, response.status_code)
