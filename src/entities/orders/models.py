from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Numeric

from src.infrastructure.postgres.base import base


class OrderModel(base):
    __tablename__ = "orders"

    id = Column(Integer(), primary_key=True)
    code = Column(Integer(), nullable=False)
    value = Column(Numeric(), nullable=False)
    cpf = Column(String(11), nullable=False)
    status = Column(String(20), nullable=True, default="In validation")
    date = Column(DateTime(), default=datetime.now)
    created_at = Column(DateTime(), default=datetime.now)
    updated_at = Column(DateTime(), default=datetime.now, onupdate=datetime.now)

    def to_dict(self):
        return dict(
            [
                (k, getattr(self, k))
                for k in self.__dict__.keys()
                if not k.startswith("_")
            ]
        )
