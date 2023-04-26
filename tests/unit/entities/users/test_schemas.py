import unittest
from unittest.mock import patch

import pytest

from src.entities.users.schemas import UserRegisterSchema


class TestUserSchemas(unittest.TestCase):
    def test_user_register(self):
        valid_user = UserRegisterSchema(
            **{
                "full_name": "Full Name",
                "email": "email@email.com",
                "cpf": "12312312312",
                "password": "password",
                "disabled": False,
            }
        )

        self.assertEqual(len(valid_user.dict().keys()), 5)

    def test_user_register_with_invalid_cpf(self):
        with pytest.raises(ValueError) as excinfo:
            UserRegisterSchema(
                **{
                    "full_name": "Full Name",
                    "email": "email@email.com",
                    "cpf": "invalid_value",
                    "password": "password",
                    "disabled": False,
                }
            )

        self.assertEqual(
            excinfo.value.errors()[0]["msg"], "CPF deve conter 11 caracteres"
        )
