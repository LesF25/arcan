from typing import Optional, Any

import phonenumbers
from pydantic import (
    BaseModel,
    EmailStr,
    field_validator,
    model_validator,
    ConfigDict,
)
from werkzeug.security import generate_password_hash

from src.utils.types import OrderType, UserOrderFields, RoleName
from .base import BaseCollectionRequestParams
from .structures import Password, PasswordUpdate


class UserBaseModel(BaseModel):
    login: str
    status: bool
    full_name: str
    email: EmailStr
    phone_number: str
    client_id: Optional[int] = None
    role_id: int

    @field_validator('phone_number', mode='after')
    def _validate_phone_number(cls, value: str):
        phone = phonenumbers.parse(value)
        if not phonenumbers.is_valid_number(phone):
            raise ValueError('Invalid data: Incorrect phone number.')

        return value

    @model_validator(mode='after')
    def _validate_model(self):
        if (
            self.role_id == 1
            and self.client_id is None
        ):
            raise ValueError("Invalid data: client's company is missing")

        return self


class CreateUserSchema(UserBaseModel):
    password: Password


class UserResponseSchema(UserBaseModel):
    id: int
    role_name: RoleName
    client_name: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class UpdateUserSchema(BaseModel):
    login: Optional[str] = None
    password: Optional[PasswordUpdate] = None
    status: Optional[bool] = None
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = None

    @field_validator('phone_number', mode='after')
    def _validate_phone_number(
        cls,
        value: str | None
    ) -> str | None:
        if value is None:
            return value

        phone = phonenumbers.parse(value)
        if not phonenumbers.is_valid_number(phone):
            raise ValueError('Invalid data: Incorrect phone number.')

        return value

    def validate_password(
        self,
        valid_password_hash: str,
    ) -> None:
        if generate_password_hash(self.password.old_password) != valid_password_hash:
            raise ValueError('InvalidData: incorrect password.')

    def model_dump(
        self,
        *args: Any,
        **kwargs: Any,
    ) -> dict[str, Any]:
        data = super().model_dump(*args, **kwargs)
        for key, val in data.items():
            if val is None:
                del data[key]

        if not data:
            raise ValueError('Необходимо указать хотя бы один параметр для изменения.') #TODO: fix text error

        return data


class GetUserSchema(BaseCollectionRequestParams):
    order_by: Optional[
        dict[UserOrderFields, OrderType]
    ] = {'id': 'ASC'}


class DeleteUserSchema(BaseModel):
    ids: list[int]

    ROOT_USER_ID = 1
    DELETE_USER_ID = 2

    @field_validator('ids', mode='after')
    def _validate_ids(self, value: list[int]):
        if not value:
            raise ValueError()  # TODO

        if (
            self.ROOT_USER_ID in value
            or self.DELETE_USER_ID in value
        ):
            raise ValueError('')  # TODO

        return value
