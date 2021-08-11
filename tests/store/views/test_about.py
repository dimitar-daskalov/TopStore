from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

UserModel = get_user_model()


class AboutTests(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user(
            email='test@user.user',
            username='test_user',
            password='test_user',
        )

    def test_AboutTemplate_expectToBeCorrect(self):
        response = self.client.get(reverse('about'))
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'store/about.html')

    def test_AboutWhenAuthenticatedUser_expectToShowAboutSuccessfully(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('about'))
        self.assertEqual(200, response.status_code)

    def test_AboutWhenNotAuthenticatedUser_expectToShowAboutSuccessfully(self):
        response = self.client.get(reverse('about'))
        self.assertEqual(200, response.status_code)
