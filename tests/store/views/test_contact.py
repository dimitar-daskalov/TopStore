from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from TopStore.store.models import ContactMessage

UserModel = get_user_model()


class ContactTests(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user(
            email='test@user.user',
            username='test_user',
            password='test_user',
        )
        self.contact_message = ContactMessage.objects.create(
            name='test_user',
            email='test@user.user',
            message='test_user message',
            answered='False',
        )

    def test_ContactTemplate_expectToBeCorrect(self):
        response = self.client.get(reverse('contact'))
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'store/contact.html')

    def test_ContactWhenAuthenticatedUser_expectToShowContactSuccessfully(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('contact'))
        self.assertEqual(200, response.status_code)

    def test_ContactWhenNotAuthenticatedUser_expectToShowContactSuccessfully(self):
        response = self.client.get(reverse('contact'))
        self.assertEqual(200, response.status_code)

    def test_ContactWhenUserSendMessage_expectToSaveContactMessageSuccessfully(self):
        self.assertTrue(self.contact_message)
