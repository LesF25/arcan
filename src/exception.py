import json


class DeleteError(Exception):
    def __init__(
        self,
        message: str,
        original_error: str,
    ) -> None:
        message = json.dumps({
            'success': False,
            'message': message,
            'error': original_error
        })
        super().__init__(message)
