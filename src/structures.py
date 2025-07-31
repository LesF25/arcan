from typing import Callable
import dataclasses


@dataclasses.dataclass(frozen=True)
class Rule:
    rule: str
    view_func: Callable
    methods: list[str]

    def as_dict(self) -> dict:
        return dataclasses.asdict(self)
