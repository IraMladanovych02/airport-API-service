from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token

from django.contrib.auth import get_user_model

from airport.models import Plane, Trip, Service, Order


class BaseTestSetup(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_superuser(
            email="admin@test.com", password="testpassword"
        )
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)


class PlaneViewSetTest(BaseTestSetup):
    def setUp(self):
        super().setUp()
        self.plane = Plane.objects.create(info="Boeing 747", num_seats=150)
        self.planes_url = reverse("airport:plane-list")
        self.plane_detail_url = reverse("airport:plane-detail", kwargs={"pk": self.plane.pk})

    def test_list_planes(self):
        response = self.client.get(self.planes_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_plane(self):
        response = self.client.get(self.plane_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_plane(self):
        data = {"info": "Airbus A320", "num_seats": 180}
        response = self.client.post(self.planes_url, data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_plane(self):
        data = {"info": "Boeing 737", "num_seats": 160}
        response = self.client.put(self.plane_detail_url, data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_plane(self):
        response = self.client.delete(self.plane_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class TripViewSetTest(BaseTestSetup):
    def setUp(self):
        super().setUp()
        self.plane = Plane.objects.create(info="Boeing 747", num_seats=150)
        self.trip = Trip.objects.create(
            source="City A", destination="City B", departure="2024-10-01 10:00:00", plane=self.plane
        )
        self.trips_url = reverse("airport:trip-list")
        self.trip_detail_url = reverse("airport:trip-detail", kwargs={"pk": self.trip.pk})

    def test_list_trips(self):
        response = self.client.get(self.trips_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_trip(self):
        response = self.client.get(self.trip_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_trip(self):
        data = {
            "source": "City C",
            "destination": "City D",
            "departure": "2024-12-01 12:00:00",
            "plane": self.plane.id,
        }
        response = self.client.post(self.trips_url, data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_trip(self):
        data = {
            "source": "City E",
            "destination": "City F",
            "departure": "2024-12-05 14:00:00",
            "plane": self.plane.id,
        }
        response = self.client.put(self.trip_detail_url, data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_trip(self):
        response = self.client.delete(self.trip_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class ServiceViewSetTest(BaseTestSetup):
    def setUp(self):
        super().setUp()
        self.service = Service.objects.create(name="Wi-Fi")
        self.services_url = reverse("airport:service-list")
        self.service_detail_url = reverse("airport:service-detail", kwargs={"pk": self.service.pk})

    def test_list_services(self):
        response = self.client.get(self.services_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_service(self):
        response = self.client.get(self.service_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_service(self):
        data = {"name": "Drinks"}
        response = self.client.post(self.services_url, data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_service(self):
        data = {"name": "Free Drinks"}
        response = self.client.put(self.service_detail_url, data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_service(self):
        response = self.client.delete(self.service_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class OrderViewSetTest(BaseTestSetup):
    def setUp(self):
        super().setUp()
        self.order = Order.objects.create(user=self.user)
        self.orders_url = reverse("airport:order-list")
        self.order_detail_url = reverse("airport:order-detail", kwargs={"pk": self.order.pk})

    def test_list_orders(self):
        response = self.client.get(self.orders_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_order(self):
        response = self.client.get(self.order_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_order(self):
        data = {"user": self.user.id}
        response = self.client.post(self.orders_url, data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_order(self):
        data = {"user": self.user.id}
        response = self.client.put(self.order_detail_url, data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_order(self):
        response = self.client.delete(self.order_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
