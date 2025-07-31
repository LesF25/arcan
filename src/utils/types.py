from typing import Annotated, Literal

from pydantic import StringConstraints

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
