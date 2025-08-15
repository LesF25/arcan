from datetime import timedelta, datetime

from dateutil.relativedelta import relativedelta
from jwt import encode
from typing_extensions import Any

import settings


class BaseTokenPolicy:
    def create_token(
        self,
        payload: dict[str, Any],
    ) -> str:
        now = datetime.utcnow()
        return encode(
            payload={
                **payload,
                'exp': now + self._expire,
                'iat': now,
            },
            key=settings.SECRET_KEY,
            algorithm='HS256',
        )

    @property
    def _expire(self) -> timedelta | relativedelta:
        raise NotImplemented()


class AccessTokenPolicy(BaseTokenPolicy):
    @property
    def _expire(self) -> timedelta | relativedelta:
        return timedelta(days=15)


class RefreshTokenPolicy(BaseTokenPolicy):
    @property
    def _expire(self) -> timedelta | relativedelta:
        return relativedelta(months=1)


class TokenPolicyFactory:
    TOKEN_POLICIES = {
        'access': AccessTokenPolicy,
        'refresh': RefreshTokenPolicy,
    }

    @classmethod
    def get_policy(cls, token_type: str) -> BaseTokenPolicy:
        return cls.TOKEN_POLICIES[token_type]
