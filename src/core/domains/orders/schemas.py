from datetime import datetime
from typing import Optional

from pydantic import Field, BaseModel, validator


class CreateOrderSchema(BaseModel):
    code: int = Field(example=1589)
    value: float = Field(example=22.5)
    cpf: str = Field(max_length=11, example="12312312312")
    date: str = Field(example=datetime.now(), default=datetime.now())

    @validator("cpf")
    def cpf_have_right_len(cls, cpf):
        if len(cpf) != 11:
            raise ValueError("CPF deve conter 11 caracteres")

        return cpf


class OrderSchema(BaseModel):
    code: int = Field(example=1589)
    value: float = Field(example=22.5)
    cpf: str = Field(max_length=11, example="12312312312")
    date: str = Field(example=datetime.now(), default=datetime.now())
    status: str = Field(example="Em validação", default="Em validação")
    created_at: str = Field(example=datetime.now(), default=datetime.now())
    updated_at: str = Field(example=datetime.now(), default=datetime.now())

    @validator("cpf")
    def cpf_have_right_len(cls, cpf):
        if len(cpf) != 11:
            raise ValueError("CPF deve conter 11 caracteres")

        return cpf


class OrderInDBSchema(BaseModel):
    code: int = Field(example=1589)
    value: float = Field(example=22.5)
    cpf: str = Field(max_length=11, example="12312312312")
    date: datetime = Field(example=datetime.now(), default=datetime.now())
    status: str = Field(example="Em validação", default="Em validação")
    created_at: datetime = Field(example=datetime.now(), default=datetime.now())
    updated_at: datetime = Field(example=datetime.now(), default=datetime.now())

    @validator("cpf")
    def cpf_have_right_len(cls, cpf):
        if len(cpf) != 11:
            raise ValueError("CPF deve conter 11 caracteres")

        return cpf


class PublicOrderSchema(BaseModel):
    code: int = Field(example=1589)
    value: float = Field(example=22.5)
    date: datetime = Field(example=datetime.now(), default=datetime.now())
    cashback_pct: str = Field(max_length=10, example="10%")
    cashback_value: float = Field(example=2.25)
    status: str = Field(example="Em validação", default="Em validação")
