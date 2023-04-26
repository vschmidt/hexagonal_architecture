import pytest
import unittest
from unittest.mock import patch
from datetime import datetime

from src.entities.orders.schemas import (
    CreateOrderSchema,
    OrderSchema,
    PublicOrderSchema,
)
from src.entities.orders.services import OrderService


@patch("src.entities.orders.services.OrderRepository")
class TestUserService(unittest.TestCase):
    def test_get_all_orders_cashback_values(self, repository_mock):
        orders = [
            PublicOrderSchema(
                **{
                    "code": 1589,
                    "value": 999,
                    "cpf": "15350946056",
                    "date": str(datetime.utcnow()),
                    "cashback_value": 99.9,
                    "cashback_pct": "10%",
                }
            ),
            PublicOrderSchema(
                **{
                    "code": 1589,
                    "value": 1010,
                    "cpf": "15350946056",
                    "date": str(datetime.utcnow()),
                    "cashback_value": 151.5,
                    "cashback_pct": "15%",
                }
            ),
            PublicOrderSchema(
                **{
                    "code": 1589,
                    "value": 5000,
                    "cpf": "15350946056",
                    "date": str(datetime.utcnow()),
                    "cashback_value": 1000.0,
                    "cashback_pct": "20%",
                }
            ),
        ]

        repository_mock.get_all_orders.return_value = orders

        response = OrderService.get_all_orders()

        for order_with_cashback, order in zip(response, orders):
            self.assertEqual(order_with_cashback.cashback_value, order.cashback_value)
            self.assertEqual(order_with_cashback.cashback_pct, order.cashback_pct)

    def test_create_order(self, repository_mock):
        order = CreateOrderSchema(
            **{
                "code": 1589,
                "value": 22.5,
                "cpf": "12345645600",
                "date": str(datetime.utcnow()),
            }
        )
        order_to_save = OrderSchema(**order.dict())
        order_to_save.status = "Em validação"

        repository_mock.create_new_order.return_value = None

        response = OrderService.create_order(order)

        self.assertIsNone(response)

        repository_mock.create_new_order.assert_called_once_with(order_to_save)

    def test_create_order_with_auto_approval(self, repository_mock):
        order = CreateOrderSchema(
            **{
                "code": 1589,
                "value": 22.5,
                "cpf": "15350946056",
                "date": str(datetime.utcnow()),
            }
        )
        order_to_save = OrderSchema(**order.dict())
        order_to_save.status = "Aprovado"

        repository_mock.create_new_order.return_value = None

        response = OrderService.create_order(order)

        self.assertIsNone(response)

        repository_mock.create_new_order.assert_called_once_with(order_to_save)
