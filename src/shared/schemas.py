from pydantic import BaseModel


class TokenInfos(BaseModel):
    email: str
    cpf: str
    exp: str
