from typing import Callable

from flask import Response
from pydantic import ValidationError

from src.exception import DeleteError
from src.utils import json_helpers

__error_handler_registry: dict[type[Exception], type['BaseErrorHandler']] = {}


def get_error_handler_registry() -> dict[type[Exception], type['BaseErrorHandler']]:
    return __error_handler_registry


def get_handler_by_error(error: Exception) -> 'BaseErrorHandler':
    registry = get_error_handler_registry()
    error_handler = registry.get(type(error), DefaultErrorHandler)

    return error_handler()


def add_error_handler(error_type: type[Exception]) -> Callable[[type['BaseErrorHandler']], type['BaseErrorHandler']]:
    def fn_wrapper(cls: type['BaseErrorHandler']) -> type['BaseErrorHandler']:
        registry = get_error_handler_registry()
        if error_type in registry:
            raise Exception(f'Error Handler {error_type} allready register')

        registry[error_type] = cls
        return cls

    return fn_wrapper


class BaseErrorHandler:
    def handle(
        self,
        error: Exception,
    ) -> Response:
        raise NotImplementedError


@add_error_handler(ValueError)
@add_error_handler(ValidationError)
class ValueErrorHandler(BaseErrorHandler):
    def handle(
        self,
        error: Exception,
    ) -> Response:
        response = Response(
            response=json_helpers.dumps({
                'message': (
                    'Your request contains invalid data. '
                    'Please check the provided details.'
                ),
                'detail': str(error)
            }),
            status=400,
        )

        return response


@add_error_handler(DeleteError)
class DeleteErrorHandler(BaseErrorHandler):
    def handle(
        self,
        error: Exception,
    ) -> Response:
        response = Response(
            response=json_helpers.dumps({
                'success': False,
                'message': (
                    "Couldn't delete the resource. "
                    'Please try again or contact support if the issue persists.'
                ),
                'detail': str(error),
            }),
            status=500,
        )

        return response


class DefaultErrorHandler(BaseErrorHandler):
    def handle(
        self,
        error: Exception,
    ) -> Response:
        response = Response(
            response=json_helpers.dumps({
                'message': 'Something went wrong. Please contact Sinthy Support.',
                'detail': str(error)
            }),
            status=500,
        )

        return response
