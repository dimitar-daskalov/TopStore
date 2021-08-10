from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

UserModel = get_user_model()


class SignInUserTests(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user(
            email='test@user.user',
            username='test_user',
            password='test_user',
        )

    def test_SignInTemplate_expectToBeCorrect(self):
        response = self.client.get(reverse('sign in user'))
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'account/sign_in_user.html')

    def test_SignInWhenAuthenticatedUser_expectToRedirect(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('sign in user'))
        self.assertEqual(302, response.status_code)

    def test_SignInWhenNotAuthenticatedUser_expectToSignInSuccessfully(self):
        response = self.client.post(reverse('sign in user'))
        self.assertEqual(self.user.email, UserModel.objects.get(pk=self.user.id).email)
        self.assertEqual(200, response.status_code)
