import contextlib
from typing import Generator

from flask import Response
from flask.views import MethodView
from flask_pydantic import validate
from sqlalchemy.exc import SQLAlchemyError

from wsgi import app
from src.structures import Rule
from src.schemas.user import (
    UserGetSchema,
    UserCreateSchema,
    UserUpdateSchema,
    UserDeleteSchema,
)
from src.services.user import UserService
from src.utils import json_helpers
from src.exception import DeleteError
from . import rules


class BaseUserView(MethodView):
    @property
    @contextlib.contextmanager
    def _user_service(self) -> Generator:
        with app.database.session() as session:
            yield UserService(session)


class UserView(BaseUserView):
    @validate(body=UserCreateSchema)
    def post(self, body: UserCreateSchema) -> Response:
        with self._user_service as service:
            user = service.create_user(body)
            response = Response(
                status=200,
                response=json_helpers.dumps({
                    'user': user,
                }),
            )

            return response

    @validate(query=UserGetSchema)
    def get(self, query: UserGetSchema) -> Response:
        with self._user_service as service:
            total_page, users = service.get_users(query)

            response = Response(
                status=200,
                response=json_helpers.dumps({
                    'users': users,
                    'page': query.page,
                    'page_size': query.page_size,
                    'total_page': total_page,
                }),
            )

            return response

    @validate(query=UserDeleteSchema)
    def delete(
        self,
        query: UserDeleteSchema,
    ) -> Response:
        with self._user_service as service:
            try:
                success = service.delete_user(query)
            except SQLAlchemyError as e:
                raise DeleteError(str(e))

            response = Response(
                status=200,
                response=json_helpers.dumps({
                    'success': success,
                }),
            )

            return response


class UserByIdView(BaseUserView):
    def get(
        self,
        user_id: int,
    ) -> Response:
        with self._user_service as service:
            user = service.get_user_by_id(user_id)
            response = Response(
                status=200,
                response=json_helpers.dumps({
                    'user': user,
                }),
            )

            return response

    @validate(body=UserUpdateSchema)
    def patch(
        self,
        body: UserUpdateSchema,
        user_id: int,
    ) -> Response:
        with self._user_service as service:
            user = service.update_user(body, user_id)
            response = Response(
                status=200,
                response=json_helpers.dumps({
                    'user': user,
                }),
            )

            return response


rules.extend([
    Rule(
        rule='/users',
        view_func=UserView.as_view('users'),
        methods=['GET', 'POST', 'DELETE']
    ),
    Rule(
        rule='/users/<int:user_id>',
        view_func=UserByIdView.as_view('user'),
        methods=['GET', 'PATCH']
    ),
])
