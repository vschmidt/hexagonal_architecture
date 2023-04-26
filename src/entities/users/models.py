from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean

from src.infrastructure.postgres.base import base


class UserModel(base):
    __tablename__ = "users"

    id = Column(Integer(), primary_key=True)
    full_name = Column(String(240), nullable=False)
    email = Column(String(240), nullable=False)
    cpf = Column(String(11), nullable=False, unique=True)
    hashed_password = Column(String(240), nullable=False)
    disabled = Column(Boolean(), nullable=False)
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
