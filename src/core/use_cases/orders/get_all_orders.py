from typing import List

from src.core.domains.orders.repository import OrderRepository
from src.core.domains.orders.schemas import (
    OrderInDBSchema,
    PublicOrderSchema,
)


class OrderService:
    @classmethod
    def get_all_orders(cls):
        orders = OrderRepository.get_all_orders()

        orders_with_cashback_applied = cls.__append_cashback_values(orders)

        return orders_with_cashback_applied

    @classmethod
    def __append_cashback_values(cls, orders: List[OrderInDBSchema]):
        orders_with_cashback_applied = []

        for order in orders:
            order_with_cashback = order.dict()

            cashback_pct = cls.__calculate_cashback_pct(order)

            order_with_cashback["cashback_value"] = order.value * cashback_pct
            order_with_cashback["cashback_pct"] = f"{int(cashback_pct * 100)}%"

            orders_with_cashback_applied.append(
                PublicOrderSchema(**order_with_cashback)
            )

        return orders_with_cashback_applied

    @classmethod
    def __calculate_cashback_pct(cls, order: OrderInDBSchema):
        if order.value < 1000:
            return 0.1
        elif order.value < 1500:
            return 0.15

        return 0.2
