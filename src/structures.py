from typing import Callable

from pydantic import BaseModel, model_validator, ValidationError

from src.utils.types import PasswordType


class Rule(BaseModel):
    rule: str
    view_func: Callable
    methods: list[str]


class Password(BaseModel):
    password: PasswordType
    confirm_password: PasswordType

    @model_validator(mode='after')
    def _validate_password(self):
        if self.password != self.confirm_password:
            raise ValidationError('Invalid data: Incorrect password')

        return self


class PasswordUpdate(BaseModel):
    old_password: PasswordType
    new_password: PasswordType
