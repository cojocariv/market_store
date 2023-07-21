from django.test import TestCase
from django.urls import reverse


class UserRegistrationViewTestCase(TestCase):
    def setUp(self):
        self.path = reverse('users:registration')


