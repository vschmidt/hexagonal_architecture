from sqlalchemy import select, insert

from src.core.domains.orders.models import OrderModel
from src.core.domains.orders.schemas import (
    CreateOrderSchema,
    OrderInDBSchema,
)
from src.adapters.postgres.database import PostgresDatabase


class OrderRepository:
    @classmethod
    def get_all_orders(cls):
        with PostgresDatabase() as engine:
            results = engine.session.execute(select(OrderModel)).all()

        results = [OrderInDBSchema(**r[0].to_dict()) for r in results]
        return results

    @classmethod
    def create_new_order(cls, order: CreateOrderSchema):
        with PostgresDatabase() as engine:
            engine.session.execute(insert(OrderModel).values(**order.dict()))
            engine.session.commit()
