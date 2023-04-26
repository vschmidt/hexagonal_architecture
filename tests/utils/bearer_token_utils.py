from time import time

from jose import jwt

from src.settings.environment import Environment


class JWTGenerator:
    def __init__(self) -> None:
        self.env = Environment()
        self.email = "email@email.com"
        self.cpf = "12312312312"

    def generate_jwt_token(self, payload):
        token = jwt.encode(payload, self.env.SECRET_KEY, self.env.ALGORITHM)
        return token

    def generate_valid_token(self):
        payload = {"exp": time() + 100, "email": self.email, "cpf": self.cpf}
        return self.generate_jwt_token(payload)

    def generate_invalid_token(self):
        payload = {"exp": time() + 100, "email": self.email, "cpf": self.cpf}
        return self.generate_jwt_token(payload)[:5]

    def generate_expired_token(self):
        payload = {"exp": time() - 100, "email": self.email, "cpf": self.cpf}
        return self.generate_jwt_token(payload)
