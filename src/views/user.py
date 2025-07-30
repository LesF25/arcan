import contextlib
from typing import Generator

from flask import Response
from flask.views import MethodView
from flask_pydantic import validate
from sqlalchemy.exc import SQLAlchemyError

from application.app import app, Rule
from . import rules
from src.schemas.user import GetUserSchema, CreateUserSchema, UpdateUserSchema, DeleteUserSchema
from src.services.user import UserService
from src.utils import json_helpers
from ..exception import DeleteError


class BaseUserView(MethodView):
    @property
    @contextlib.contextmanager
    def _user_service(self) -> Generator:
        with app.database.session() as session:
            yield UserService(session)


class UserView(BaseUserView):
    @validate(body=CreateUserSchema)
    def post(self, body: CreateUserSchema) -> Response:
        with self._user_service as service:
            user = service.create_user(body)
            response = Response(
                status=200,
                response=json_helpers.dumps({
                    'user': user,
                }),
            )

            return response

    @validate(query=GetUserSchema)
    def get(self, query: GetUserSchema) -> Response:
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

    @validate(query=DeleteUserSchema)
    def delete(
        self,
        query: DeleteUserSchema,
    ) -> Response:
        with self._user_service as service:
            try:
                success = service.delete_user(query)
            except SQLAlchemyError as e:
                raise DeleteError(
                    message='Не удалось удалить ресурс',  #TODO
                    original_error=str(e),
                )

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

    @validate(body=UpdateUserSchema)
    def patch(
        self,
        body: UpdateUserSchema,
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
