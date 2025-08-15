from pydantic import BaseModel

from src.schemas import UserResponseSchema
from src.utils.types import PasswordType
from src.auth import Token


class AuthLoginSchema(BaseModel):
    login: str
    password: PasswordType


class AuthResponseSchema(BaseModel):
    user: UserResponseSchema
    token: Token | str
