from typing import Annotated, Optional, Literal

import phonenumbers
from pydantic import (
    StringConstraints,
    BaseModel,
    EmailStr,
    field_validator,
    model_validator, ConfigDict,
)

from .base import BaseCollectionRequestParams


UserOrderFields = Annotated[
    str,
    Literal[
        'id',
        'login',
        'status',
        'role_name',
        'client_name',
    ]
]

OrderType = Annotated[
    str,
    Literal[
        'ASC',
        'DESC',
    ],
]


class UserRequestParams(BaseCollectionRequestParams):
    order_by: Optional[
        dict[UserOrderFields, OrderType]
    ] = {'id': 'ASC'}


class UserRequestBody(BaseModel):
    login: str
    password: Annotated[
        str, StringConstraints(min_length=8)
    ]
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
    def _validate_client_id(self):
        if (
            self.role_id == 1
            and self.client_id is None
        ):
            raise ValueError("Invalid data: client's company is missing")

        return self


class UserResponseModel(UserRequestBody):
    id: int
    role_name: Annotated[
        str,
        Literal[
            'Client',
            'Administrator',
            'Operator'
        ]
    ]
    client_name: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
