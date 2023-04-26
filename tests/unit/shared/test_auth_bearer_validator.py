import unittest
from unittest.mock import Mock

from fastapi import HTTPException

from src.shared.auth_bearer_validator import AuthBearerValidator
from tests.utils.bearer_token_utils import JWTGenerator


class TestJWTBearer(unittest.IsolatedAsyncioTestCase):
    """Testing Auth Bearer Shared module"""

    def setUp(self) -> None:
        self.token_generator = JWTGenerator()

    def generate_mock_request_by_token(self, token: str):
        request = Mock()
        request.headers = {"Authorization": f"Bearer {token}"}

        return request

    async def test_request_with_valid_token(self):
        valid_token = self.token_generator.generate_valid_token()
        request = self.generate_mock_request_by_token(valid_token)

        jwt_bearer = AuthBearerValidator()
        response = await jwt_bearer.__call__(request)

        self.assertIsInstance(response, dict)

    async def test_request_with_invalid_token(self):
        invalid_token = self.token_generator.generate_invalid_token()
        request = self.generate_mock_request_by_token(invalid_token)

        jwt_bearer = AuthBearerValidator()

        try:
            await jwt_bearer.__call__(request)
        except HTTPException as err:
            self.assertEqual(err.status_code, 403)
        else:
            raise HTTPException

    async def test_request_with_expired_token(self):
        expired_token = self.token_generator.generate_expired_token()
        request = self.generate_mock_request_by_token(expired_token)

        jwt_bearer = AuthBearerValidator()

        try:
            await jwt_bearer.__call__(request)
        except HTTPException as err:
            self.assertEqual(err.status_code, 403)
        else:
            raise HTTPException
