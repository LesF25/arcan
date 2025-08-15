from typing import Any

from jwt import decode

import settings
from .token_policy import TokenPolicyFactory
from src.utils.types import TokenType


class TokenManager:
    def create_token(
        self,
        token_type: TokenType,
        payload: dict[str, Any],
    ) -> str:
        policy = TokenPolicyFactory.get_policy(token_type)
        payload.update({
            'token_type': token_type
        })

        return policy.create_token(payload)

    def decode_token(
        self,
        token: str,
    ) -> dict:
        return decode(
            jwt=token,
            key=settings.SECRET_KEY,
            algorithms=['HS256'],
        )
