from django.test import TestCase
from django.contrib.auth import get_user_model

from rest_framework.exceptions import ValidationError

from user.serializers import UserSerializer


class UserSerializerTest(TestCase):
    def setUp(self):
        self.User = get_user_model()
        self.user = self.User.objects.create_user(
            email="test@test.com", password="password"
        )
        self.serializer = UserSerializer(instance=self.user)

    def test_serializer_valid_data(self):
        data = {
            "email": "newuser@example.com",
            "password": "newpassword",
            "first_name": "New",
            "last_name": "User",
        }
        serializer = UserSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()
        self.assertEqual(user.email, "newuser@example.com")
        self.assertTrue(user.check_password("newpassword"))

    def test_serializer_update(self):
        data = {"email": "updatesuser@example.com", "password": "newpassword"}
        serializer = UserSerializer(instance=self.user, data=data, partial=True)
        self.assertTrue(serializer.is_valid(), msg="Serializer data is invalid")
        updated_user = serializer.save()

        self.assertEqual(
            updated_user.email,
            "updatesuser@example.com",
            "User email was not updated correctly",
        )
        self.assertTrue(
            updated_user.check_password("newpassword"),
            "Password was not updated correctly",
        )

    def test_serializer_invalid_password(self):
        data = {"username": "invaliduser@test.com", "password": "123"}
        serializer = UserSerializer(data=data)
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)
