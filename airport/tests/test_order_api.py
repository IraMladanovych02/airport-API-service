from rest_framework import status
from rest_framework.test import APITestCase

from django.contrib.auth import get_user_model


class OrderAPITestCase(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(email='test@test.com', password='testpassword')
        self.client.force_authenticate(user=self.user)

    def test_create_order(self):
        data = {
            "tickets": [1, 2],  # Ensure ticket IDs exist in your test DB
            "other_order_fields": "values"
        }
        response = self.client.post(data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_orders(self):
        response = self.client.get(self.order_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_order(self):
        response = self.client.delete(self.order_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_ticket_seat(self):
        data = {
            "tickets": [999],  # Non-existent ticket
            "other_order_fields": "values"
        }
        response = self.client.post(self.order_list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
