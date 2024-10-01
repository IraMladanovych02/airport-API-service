from django.test import SimpleTestCase
from django.urls import reverse, resolve

from user.views import CreateUserView, LoginUserView, CreateTokenView


class TestURLs(SimpleTestCase):

    def test_create_user_url(self):
        url = reverse("user:create")
        self.assertEqual(resolve(url).func.view_class, CreateUserView)

    def test_login_user_url(self):
        url = reverse("user:login")
        self.assertEqual(resolve(url).func.view_class, LoginUserView)

    def test_manage_user_url(self):
        url = reverse("user:manage")
        self.assertEqual(resolve(url).func.view_class, CreateTokenView)
