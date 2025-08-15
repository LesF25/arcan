from typing import Generator

from flask import Response, request
from flask_pydantic import validate
from jwt import InvalidTokenError

from src.structures import Rule
from src.schemas import AuthLoginSchema, AuthResponseSchema
from src.services import AuthService
from src.utils import json_helpers
from . import rules
from .base import BaseView


class BaseAuthView(BaseView):
    AUTH_HEADER_NAME = 'Authorization'

    @property
    def _service(self) -> Generator[AuthService, None, None]:
        return self._get_service(AuthService)

    @property
    def _token(self) -> str:
        if not (auth := request.headers.get(self.AUTH_HEADER_NAME)):
            raise InvalidTokenError('Authorization header is missing')
        _, token = auth.split(' ')

        return token


class LoginView(BaseAuthView):
    @validate(body=AuthLoginSchema)
    def post(self, body: AuthLoginSchema) -> Response:
        with self._service as service:
            login_data: AuthResponseSchema = service.login(body)
            response = Response(
                status=200,
                response=json_helpers.dumps({
                    'user': login_data.user,
                    'access_token': login_data.token,
                })
            )

            return response


class LogoutView(BaseAuthView):
    def post(self):
        with self._service as service:
            service.auth(self._token)
            ...


class AuthView(BaseAuthView):
    def post(self):
        with self._service as service:
            service.auth(self._token)
            ...


class RefreshView(BaseAuthView):
    def post(self):
        with self._service as service:
            service.refresh(self._token)
            ...


rules.extend([
    Rule(
        rule='/login',
        view_func=LoginView.as_view('login'),
        methods=['POST']
    ),
    Rule(
        rule='/logout',
        view_func=LogoutView.as_view('logout'),
        methods=['POST']
    ),
    Rule(
        rule='/auth',
        view_func=AuthView.as_view('auth'),
        methods=['POST']
    ),
    Rule(
        rule='/refresh',
        view_func=RefreshView.as_view('refresh'),
        methods=['POST']
    ),
])
