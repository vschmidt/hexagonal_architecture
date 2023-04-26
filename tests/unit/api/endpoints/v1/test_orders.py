from datetime import datetime
from fastapi import status
import unittest
from unittest.mock import patch
from fastapi.testclient import TestClient
from src.entities.orders.schemas import CreateOrderSchema

from tests.utils.bearer_token_utils import JWTGenerator


class TestOrdersV1(unittest.TestCase):
    def setUp(self):
        from src.main import app

        self.client = TestClient(app)
        self.jwt_generator = JWTGenerator()

    def test_get_all_orders_without_token(self):
        response = self.client.get("/v1/orders/get_all_orders")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch("src.api.endpoints.v1.orders.OrderService")
    def test_get_all_orders_with_valid_token(self, service_mock):
        response = self.client.get(
            "/v1/orders/get_all_orders",
            headers={
                "Authorization": f"Bearer {self.jwt_generator.generate_valid_token()}"
            },
        )

        service_mock.get_all_orders.assert_called_once()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_order_without_token(self):
        response = self.client.post("/v1/orders/create")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch("src.api.endpoints.v1.orders.OrderService")
    def test_create_order_with_valid_token(self, service_mock):
        order = CreateOrderSchema(
            **{
                "code": 1589,
                "value": 22.5,
                "cpf": "12345645600",
                "date": str(datetime.utcnow()),
            }
        ).dict()

        response = self.client.post(
            "/v1/orders/create",
            headers={
                "Authorization": f"Bearer {self.jwt_generator.generate_valid_token()}"
            },
            json=order,
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        service_mock.create_order.assert_called_once_with(order)

    @patch("src.api.endpoints.v1.orders.OrderService")
    def test_create_order_with_error_in_order_service(self, service_mock):
        order = CreateOrderSchema(
            **{
                "code": 1589,
                "value": 22.5,
                "cpf": "12345645600",
                "date": str(datetime.utcnow()),
            }
        ).dict()
        service_mock.create_order.side_effect = ValueError

        response = self.client.post(
            "/v1/orders/create",
            headers={
                "Authorization": f"Bearer {self.jwt_generator.generate_valid_token()}"
            },
            json=order,
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        service_mock.create_order.assert_called_once_with(order)
