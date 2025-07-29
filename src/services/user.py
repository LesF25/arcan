import math
from typing import Generator

from sqlalchemy.orm import Session, Query
from sqlalchemy import asc, desc, and_
from werkzeug.security import generate_password_hash

from src.models import RoleModel, ClientModel
from src.models.user import UserModel
from src.schemas.user import UserRequestBody, UserRequestParams, OrderType, UserOrderFields, UserResponseModel
from src.utils.mappers import UserMapper


class UserService:
    ROOT_USER_ID = 1
    DELETE_USER_ID = 2

    def __init__(self, session: Session):
        self.session = session

    def create_user(
        self,
        user_data: UserRequestBody,
    ) -> UserResponseModel:
        hashed_password = generate_password_hash(user_data.password)
        user = UserModel(
            **{
                **user_data.model_dump(),
                'password': hashed_password,
            }
        )
        self.session.add(user)
        self.session.flush()

        query = self._query.filter(
            UserModel.id == user.id
        )

        return UserResponseModel.from_orm(query.first())

    def get_users(
        self,
        params: UserRequestParams,
    ) -> tuple[int, list[UserResponseModel]]:
        query: Query = self._query.filter(
            UserModel.id not in [
                self.ROOT_USER_ID,
                self.DELETE_USER_ID
            ]
        )

        if search := params.search:
            query = query.filter(
                UserModel.login.ilike(f'%{search}%')
            )
        total_page = math.ceil(query.count() / params.page_size)

        query = query.order_by(*self._get_order_columns(params.order_by))
        query = (
            query
            .limit(params.page_size)
            .offset(
                (params.page - 1) * params.page_size
            )
        )
        users = [
            UserResponseModel.from_orm(user)
            for user in query.all()
        ]

        return total_page, users

    def _get_order_columns(
        self,
        order_by: dict[UserOrderFields, OrderType],
    ) -> Generator:
        for sort_column, sort_type in order_by.items():
            column = UserMapper.get_column(sort_column)
            yield (
                asc(column)
                if sort_type == 'ASC'
                else desc(column)
            )

    @property
    def _query(self) -> Query:
        return (
            self.session.query(
                UserModel,
                RoleModel.name.label('role_name'),
                ClientModel.name.label('client_name'),
            )
            .join(RoleModel, UserModel.role_id == RoleModel.id)
            .join(ClientModel, UserModel.client_id == ClientModel.id)
        )
