import time
from typing import Dict, Optional, Tuple

from jose import jwt
from fastapi import HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from src.settings.environment import Environment


class AuthBearerValidator(HTTPBearer):
    def __init__(self):
        super(__class__, self).__init__(auto_error=True)
        self.env = Environment()

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(
            __class__, self
        ).__call__(request)

        is_token_valid, decoded_token = self.verify_jwt(credentials.credentials)
        if not is_token_valid:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Token inválido ou expirado.",
            )

        return decoded_token

    def verify_jwt(self, token: str) -> Tuple[bool, Dict]:
        is_token_valid: bool = False
        payload = self.decode_jwt(token)

        if payload:
            is_token_valid = True
        return is_token_valid, payload

    def decode_jwt(self, token: str) -> Optional[dict]:
        try:
            decoded_token = jwt.decode(
                token, self.env.SECRET_KEY, algorithms=[self.env.ALGORITHM]
            )
            if "exp" in decoded_token and decoded_token["exp"] >= time.time():
                return decoded_token
            return None
        except Exception:
            return {}
