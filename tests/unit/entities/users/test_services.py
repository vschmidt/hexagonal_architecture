import unittest
from unittest.mock import Mock, patch

import pytest

from src.entities.users.schemas import UserAccumulatedCashbackSchema, UserRegisterSchema
from src.entities.users.services import UserService
from src.shared.exceptions.exceptions import ApiUnavailable, UserAlreadyExists
from src.shared.schemas import TokenInfos


class TestUserService(unittest.TestCase):
    @patch("src.entities.users.services.UserRepository")
    def test_create_user(self, repository_mock):
        valid_user = UserRegisterSchema(
            **{
                "full_name": "Full Name",
                "email": "email@email.com",
                "cpf": "12312312312",
                "password": "password",
                "disabled": False,
            }
        )
        repository_mock.get_user_by_cpf.return_value = None

        response = UserService.create_user(valid_user)

        self.assertIsNone(response)
        repository_mock.get_user_by_cpf.assert_called_once_with(valid_user.cpf)
        repository_mock.create_new_user.assert_called_once()

    @patch("src.entities.users.services.UserRepository")
    def test_create_user_already_exists(self, repository_mock):
        valid_user = UserRegisterSchema(
            **{
                "full_name": "Full Name",
                "email": "email@email.com",
                "cpf": "12312312312",
                "password": "password",
                "disabled": False,
            }
        )
        repository_mock.get_user_by_cpf.return_value = valid_user

        with pytest.raises(UserAlreadyExists):
            UserService.create_user(valid_user)

        repository_mock.get_user_by_cpf.assert_called_once_with(valid_user.cpf)

    @patch("src.entities.users.services.httpx")
    def test_get_user_cashback_with_fail(self, httpx_mock):
        httpx_mock.Client.side_effect = ApiUnavailable

        with pytest.raises(ApiUnavailable):
            UserService.get_user_cashback(
                TokenInfos(**{"email": "str", "cpf": "str", "exp": "str"})
            )

        httpx_mock.Client.assert_called_once()

    @patch("src.entities.users.services.httpx")
    def test_get_user_cashback_with_success(self, httpx_mock):
        cliente_mock = Mock()
        cliente_mock.get().json.return_value = {
            "statusCode": 200,
            "body": {"credit": 3400},
        }

        httpx_mock.Client().__enter__.return_value = cliente_mock

        response = UserService.get_user_cashback(
            TokenInfos(**{"email": "str", "cpf": "str", "exp": "str"})
        )

        self.assertIsInstance(response, UserAccumulatedCashbackSchema)
        self.assertEqual(response.accumulated_cashback, 3400)
