from typing import Callable

from pydantic import BaseModel


class Rule(BaseModel):
    rule: str
    view_func: Callable
    methods: list[str]
