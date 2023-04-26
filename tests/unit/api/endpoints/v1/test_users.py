import unittest
from unittest.mock import patch
from fastapi.testclient import TestClient
from fastapi import status

from src.entities.users.schemas import UserLoginSchema, UserRegisterSchema
from tests.utils.bearer_token_utils import JWTGenerator


class TestUsersV1(unittest.TestCase):
    def setUp(self):
        from src.main import app

        self.client = TestClient(app)
        self.jwt_generator = JWTGenerator()

    @patch("src.api.endpoints.v1.users.UserService")
    def test_create_new_user_with_success(self, service_mock):
        user = UserRegisterSchema(
            **{
                "full_name": "Full Name",
                "email": "email@email.com",
                "cpf": "12312312312",
                "password": "password",
                "disabled": False,
            }
        ).dict()

        response = self.client.post("/v1/users/create", json=user)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        service_mock.create_user.assert_called_once()

    @patch("src.api.endpoints.v1.users.UserService")
    def test_create_new_user_with_fail(self, service_mock):
        user = UserRegisterSchema(
            **{
                "full_name": "Full Name",
                "email": "email@email.com",
                "cpf": "12312312312",
                "password": "password",
                "disabled": False,
            }
        ).dict()

        service_mock.create_user.side_effect = ValueError

        response = self.client.post("/v1/users/create", json=user)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        service_mock.create_user.assert_called_once()

    @patch("src.api.endpoints.v1.users.UserService")
    def test_create_new_user_with_success(self, service_mock):
        user = UserLoginSchema(
            **{
                "cpf": "email@email.com",
                "password": "password",
            }
        ).dict()
        service_mock.token_login.return_value = "false_token"

        response = self.client.post("/v1/users/token", json=user)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        service_mock.token_login.assert_called_once_with(user)

    @patch("src.api.endpoints.v1.users.UserService")
    def test_get_me_information_without_token(self, service_mock):
        response = self.client.get("/v1/users/me")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch("src.api.endpoints.v1.users.UserService")
    def test_get_me_information_with_valid_token(self, service_mock):
        response = self.client.get(
            "/v1/users/me",
            headers={
                "Authorization": f"Bearer {self.jwt_generator.generate_valid_token()}"
            },
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        service_mock.get_current_user.assert_called_once()

    def test_get_me_accumulated_cashback_without_token(self):
        response = self.client.get("/v1/users/me/accumulated-cashback")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch("src.api.endpoints.v1.users.UserService")
    def test_get_me_accumulated_cashback(self, service_mock):
        response = self.client.get(
            "/v1/users/me/accumulated-cashback",
            headers={
                "Authorization": f"Bearer {self.jwt_generator.generate_valid_token()}"
            },
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        service_mock.get_user_cashback.assert_called_once()
