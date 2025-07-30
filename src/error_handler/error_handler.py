import json
from typing import Callable

import structlog
from flask import Response
from sqlalchemy.exc import SQLAlchemyError

from application.app import app
from src.exception import DeleteError
from src.utils import json_helpers

logger = structlog.get_logger(__name__)

__error_handler_registry = {}


def get_error_handler_registry() -> dict[Exception, 'BaseErrorHandler']:
    return __error_handler_registry


def add_error_handler(error: Exception) -> Callable[['BaseErrorHandler'], 'BaseErrorHandler']:
    def fn_wrapper(cls: 'BaseErrorHandler') -> 'BaseErrorHandler':
        registry = get_error_handler_registry()
        if error in registry:
            raise Exception(f'Error Handler {error.__name__} allready register')

        registry[error] = cls
        return cls

    return fn_wrapper


class BaseErrorHandler:
    def handle(
        self,
        error: Exception,
    ) -> Response:
        raise NotImplementedError


@add_error_handler(SQLAlchemyError)
class SQLAlchemyErrorHandler(BaseErrorHandler):
    def handle(
        self,
        error: Exception,
    ) -> Response:
        response = Response(
            response=json_helpers.dumps({
                'error': str(error)
            }),
            status=500,
        )

        return response


@add_error_handler(ValueError)
class ValueErrorHandler(BaseErrorHandler):
    def handle(
        self,
        error: Exception,
    ) -> Response:
        response = Response(
            response=json_helpers.dumps({
                'error': str(error)
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
            # Исключение содержит json.dumps
            response=str(error),
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
                'error': 'Something went wrong. Please contact Sinthy Support.'
            }),
            status=500,
        )

        return response


@app.errorhandler(Exception)
def handle_error(error: Exception):
    logger.error('Error', error_message=str(error), exc_info=True)
    registry = get_error_handler_registry()

    error_handler_type: type[BaseErrorHandler] = registry.get(error, DefaultErrorHandler)
    error_handler = error_handler_type()

    return error_handler.handle(error)
