from typing import Optional

from flask import Response
from flask_pydantic import validate

from application.app import app, Rule
from . import rules
from src.models.user import UserModel
from src.schemas.user import UserRequestBody, UserRequestParams
from src.services.user import UserService
from .base import BaseView
from .. import json_helpers


class UserView(BaseView):
    @validate(body=UserRequestBody)
    def post(self, body: UserRequestBody) -> Response:
        with app.database.session() as session:
            user_service = UserService(session)
            user = user_service.create_user(body)

            response = Response(
                status=200,
                response=json_helpers.dumps({
                    'user': user,
                }),
            )

            return response

    @validate(query=UserRequestParams)
    def get(self, query: UserRequestParams) -> Response:
        with app.database.session() as session:
            user_service = UserService(session)
            total_page, users = user_service.get_users(query)

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


class UserByIdView(BaseView):
    @validate()
    def get(
        self,
        user_id: Optional[int] = None,
    ) -> list[UserModel]:
        with app.database.session() as session:
            user_service = UserService(session)
            user = user_service.get_user_by_id(user_id)

            response = Response(
                status=200,
                response=json_helpers.dumps({
                    'user': user,
                }),
            )

            return response

    @validate()
    def put(self) -> UserModel:
        ...

    @validate()
    def delete(self) -> bool:
        ...


rules.extend([
    Rule(
        rule='/users',
        view_func=UserView.as_view('users'),
        methods=['GET', 'POST']
    ),
    Rule(
        rule='/users/<int:user_id>',
        view_func=UserByIdView.as_view('user'),
        methods=['GET', 'POST', 'PUT']
    ),
])
