from src.utils import json_helpers


class DeleteError(Exception):
    def __init__(
        self,
        message: str,
    ) -> None:
        super().__init__(message)
