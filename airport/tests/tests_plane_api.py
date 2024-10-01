from django.contrib.auth import get_user_model
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.reverse import reverse

from airport.models import Plane, Service
from airport.serializers import PlaneSerializer, PlaneListSerializer

PLANE_URL = reverse("airport:plane-list")


def detail_url(plane_id):
    return reverse("airport:plane-detail", args=["plane_id"])


def sample_plane(**params) -> Plane:
    defaults = {
        "info": "Airbus A380-800",
        "num_seats": 400,
    }
    defaults.update(params)
    return Plane.objects.create(**defaults)


class Unauthenticated(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(PLANE_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class Authenticated(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@test.test", password="testpassword"
        )
        self.client.force_authenticate(self.user)

    def test_planes_list(self):
        sample_plane()
        plane_with_services = sample_plane()

        service_1 = Service.objects.create(name="WIFI")
        service_2 = Service.objects.create(name="drinks")

        plane_with_services.services.add(service_1, service_2)

        res = self.client.get(PLANE_URL)
        planes = Plane.objects.all()
        serializer = PlaneListSerializer(planes, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer.data, res.data)

    def test_filter_planes(self):
        plane_without_services = sample_plane()
        plane_including_service_1 = sample_plane(info="Airbus A380-800")
        plane_including_service_2 = sample_plane(info="Airbus A800-800")

        service_1 = Service.objects.create(name="WIFI")
        service_2 = Service.objects.create(name="drinks")

        plane_including_service_1.services.add(service_1)
        plane_including_service_2.services.add(service_2)

        res = self.client.get(PLANE_URL)  # No filter
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        serializer_without_services = PlaneListSerializer(plane_without_services)
        serializer_plane_facility_1 = PlaneListSerializer(plane_including_service_1)
        serializer_plane_facility_2 = PlaneListSerializer(plane_including_service_2)

        self.assertIn(serializer_without_services.data, res.data)
        self.assertIn(serializer_plane_facility_1.data, res.data)
        self.assertIn(serializer_plane_facility_2.data, res.data)

        res = self.client.get(PLANE_URL, {"services": f"{service_1.id},{service_2.id}"})
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        self.assertIn(serializer_plane_facility_1.data, res.data)
        self.assertIn(serializer_plane_facility_2.data, res.data)
        self.assertNotIn(serializer_without_services.data, res.data)

    def test_items_retrieve(self) -> None:
        plane = Plane.objects.create(info="Airbus A380-800", num_seats=400)
        url = reverse("airport:plane-detail", args=[plane.id])
        res = self.client.get(url)

        serializer = PlaneSerializer(plane)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer.data, res.data)


class AdminBusTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="admin@admin.test", password="testpassword", is_staff=True
        )
        self.client.force_authenticate(self.user)

    def test_plane_create(self):
        payload = {"info": "Airbus A380-800", "num_seats": 400}
        res = self.client.post(PLANE_URL, payload)

        plane = Plane.objects.get(pk=res.data["id"])

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        for key in payload:
            self.assertEqual(payload[key], getattr(plane, key))

    def test_create_plane_with_service(self):
        service_1 = Service.objects.create(name="WIFI")
        service_2 = Service.objects.create(name="drinks")

        payload = {
            "info": "Airbus A380-800",
            "num_seats": 400,
            "services": [service_1.id, service_2.id],
        }
        res = self.client.post(PLANE_URL, payload)

        plane = Plane.objects.get(id=res.data["id"])
        services = plane.services.all()

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertIn(service_1, services)
        self.assertIn(service_2, services)
        self.assertEqual(services.count(), 2)
