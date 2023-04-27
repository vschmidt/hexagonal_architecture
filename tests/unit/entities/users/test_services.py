import unittest
from unittest.mock import Mock, patch

import pytest

from src.core.domains.users.schemas import (
    UserAccumulatedCashbackSchema,
    UserRegisterSchema,
)
from src.core.use_cases.users.services import UserService
from src.shared.exceptions.exceptions import ApiUnavailable, UserAlreadyExists
from src.shared.schemas import TokenInfos


class TestUserService(unittest.TestCase):
    @patch("src.core.domains.users.services.UserRepository")
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

    @patch("src.core.domains.users.services.UserRepository")
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
