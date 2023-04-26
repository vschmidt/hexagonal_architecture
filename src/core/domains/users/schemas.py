from pydantic import BaseModel, validator, Field


class UserSchema(BaseModel):
    full_name: str = Field(example="Guts")
    email: str = Field(example="email@example.com")
    cpf: str = Field(example="12312312312")
    disabled: bool = Field(False, example=False)

    @validator("cpf")
    def cpf_have_right_len(cls, cpf):
        if len(cpf) != 11:
            raise ValueError("CPF deve conter 11 caracteres")

        return cpf


class UserRegisterSchema(UserSchema):
    password: str = Field(example="Minhasenhasuperforte!1")


class UserInDBSchema(UserSchema):
    hashed_password: str


class UserLoginSchema(BaseModel):
    cpf: str = Field(example="12312312312")
    password: str = Field(example="Minhasenhasuperforte!1")


class UserAccumulatedCashbackSchema(BaseModel):
    cpf: str = Field(example="12312312312")
    accumulated_cashback: float = Field(example=20.22)
