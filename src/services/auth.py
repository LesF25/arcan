from functools import cached_property

from sqlalchemy.orm import Session
from werkzeug.security import check_password_hash

from src.exception import AuthError, PermissionError
from src.models import UserModel
from src.schemas import (
    AuthLoginSchema,
    AuthResponseSchema,
    UserResponseSchema,
)
from src.auth import TokenManager, Token
from src.services.base import BaseService


class AuthService(BaseService):
    ACCESS_TOKEN_TYPE = 'access'
    REFRESH_TOKEN_TYPE = 'refresh'

    def login(
        self,
        user_data: AuthLoginSchema,
    ) -> AuthResponseSchema:
        user = (
            self._session.query(UserModel)
            .filter(UserModel.login == user_data.login)
        ).first()

        if (
            not user
            or not check_password_hash(user.password, user_data.password)
        ):
            raise AuthError('Invalid credentials. Check please your login or password.')

        if not user.status:
            raise PermissionError('Account is inactive or blocked.')

        access_token = self._create_access_token(user)
        refresh_token = self._create_refresh_token(user)

        # TODO: redis cache

        return AuthResponseSchema(
            user=UserResponseSchema.from_orm(user),
            token=Token(
                access_token=access_token,
                refresh_token=refresh_token
            ),
        )

    def auth(self, token: str) -> UserResponseSchema:
        payload = self._token_service.decode_token(token)
        if payload['token_type'] != self.ACCESS_TOKEN_TYPE:
            raise AuthError('Invalid token')

        user = (
            self._session
            .query(UserModel)
            .filter(UserModel.id == payload['sub'])
        ).first()

        if not user:
            raise AuthError('Invalid token')

        return UserResponseSchema.from_orm(user)

    def refresh(self, token: str) -> AuthResponseSchema:
        payload = self._token_service.decode_token(token)
        if payload['token_type'] != self.REFRESH_TOKEN_TYPE:
            raise AuthError('Invalid token')

        user = (
            self._session
            .query(UserModel)
            .filter(UserModel.id == payload['sub'])
        ).first()

        if not user:
            raise AuthError('Invalid token.')

        access_token = self._create_access_token(user)

        # TODO: redis cache

        return AuthResponseSchema(
            user=UserResponseSchema.from_orm(user),
            token=access_token
        )

    def logout(self):
        # TODO: получение payload,
        #  проверка и затем удаление из кэша
        #  всех пользовательских данных
        ...

    def _create_access_token(self, user: UserModel) -> str:
        return self._token_service.create_token(
            self.ACCESS_TOKEN_TYPE,
            payload={
                'sub': user.id,
                'login': user.login,
                'role_name': user.role.name,
                'client_name': user.client.name,
            },
        )

    def _create_refresh_token(self, user: UserModel) -> str:
        return self._token_service.create_token(
            self.REFRESH_TOKEN_TYPE,
            payload={
                'sub': user.id,
            }
        )

    @cached_property
    def _token_service(self) -> TokenManager:
        return TokenManager()
