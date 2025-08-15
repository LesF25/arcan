from typing import Annotated, Literal, TypeVar

from pydantic import StringConstraints

from src.services import BaseService


ServiceType = TypeVar('ServiceType', bound=BaseService)

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

PasswordType = Annotated[
    str,
    StringConstraints(min_length=8)
]

RoleName = Annotated[
    str,
    Literal[
        'Client',
        'Administrator',
        'Operator'
    ]
]


TokenType = Annotated[
    str,
    Literal[
        'access',
        'refresh'
    ]
]
