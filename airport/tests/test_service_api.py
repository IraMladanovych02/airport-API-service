from django.test import TestCase

from airport.models import Service


class ServiceModelTest(TestCase):

    def setUp(self):
        self.service = Service.objects.create(
            name="Wi-Fi",
        )

    def test_service_creation(self):
        """Test that a service can be successfully created."""
        self.assertEqual(self.service.name, "Wi-Fi")

    def test_service_str_method(self):
        """Test the string representation of the Service model."""
        self.assertEqual(str(self.service), "Wi-Fi")
