import math
from typing import Generator

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, Query
from sqlalchemy import asc, desc, or_
from werkzeug.security import generate_password_hash

from src.models import RoleModel, ClientModel
from src.models.user import UserModel
from src.schemas.structures import PasswordUpdate
from src.schemas.user import CreateUserSchema, GetUserSchema, UserResponseSchema, UpdateUserSchema, DeleteUserSchema
from src.utils.mappers import UserMapper
from src.utils.types import UserOrderFields, OrderType


class UserService:
    DELETED_USER_ID = 2

    def __init__(self, session: Session):
        self.session = session

    def create_user(
        self,
        user_data: CreateUserSchema,
    ) -> UserResponseSchema:
        hashed_password = generate_password_hash(
            user_data.password.password
        )
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

        return UserResponseSchema.from_orm(
            query.first()
        )

    def get_users(
        self,
        params: GetUserSchema,
    ) -> tuple[int, list[UserResponseSchema]]:
        query = self._query

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
            UserResponseSchema.from_orm(user)
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

    def get_user_by_id(
        self,
        user_id: int,
    ) -> UserResponseSchema:
        user = self._query.filter(UserModel.id == user_id).first()

        return UserResponseSchema.from_orm(user)

    def update_user(
        self,
        user_data: UpdateUserSchema,
        user_id: int,
    ) -> UserResponseSchema:
        user: UserModel = self._query.filter(UserModel.id == user_id).first()
        user_data.validate_password(user.password)

        data = (
            {
                **user_data.model_dump(),
                'password': generate_password_hash(
                    password=user_data.password.new_password
                )
            }
            if user_data.password is not None
            else user_data.model_dump()
        )

        # TODO: протестировать косяк с записью bool в status
        for key, val in data:
            setattr(user, key, val)

        self.session.add(user)
        self.session.flush()

        return UserResponseSchema.from_orm(user)

    def delete_user(
        self,
        params: DeleteUserSchema,
    ) -> bool:
        self.session.query(UserModel).filter(
            UserModel.id.in_(params.ids)
        ).delete()

        return True

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
            .filter(UserModel.id != self.DELETED_USER_ID)
        )
