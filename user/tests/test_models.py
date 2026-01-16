from django.test import TestCase
from django.contrib.auth import get_user_model


class UserModelTest(TestCase):
    def setUp(self):
        self.User = get_user_model()
        self.user = self.User.objects.create_user(
            email="test@test.com", password="password"
        )

    def test_user_creation(self):
        self.assertEqual(self.user.email, "test@test.com")
        self.assertTrue(self.user.check_password("password"))

    def test_user_string_representation(self):
        self.assertEqual(str(self.user), "test@test.com")
