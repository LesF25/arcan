import structlog
from sqlalchemy.exc import SQLAlchemyError
from flask import Response

from application.app import app
import json_helpers

logger = structlog.get_logger(__name__)


class BaseErrorHandler:
    def handle(
        self,
        error: type[Exception],
    ) -> Response:
        raise NotImplementedError


class SQLAlchemyErrorHandler(BaseErrorHandler):
    def handle(
        self,
        error: type[Exception],
    ) -> Response:
        response = Response(
            response=json_helpers.dumps({

            }),
            status=500,
        )

        return response


class DefaultErrorHandler(BaseErrorHandler):
    def handle(
        self,
        error: type[Exception],
    ) -> Response:
        response = Response(
            response='Something went wrong. Please contact Sinthy Support.',
            status=500,
        )

        return response


error_handler_map = {}


@app.errorhandler(Exception)
def handle_error(error: type[Exception]):
    logger.error(
        'Error',
        error_message=str(error),
    )

    error_handler: BaseErrorHandler = error_handler_map.get(error, DefaultErrorHandler)
    return error_handler.handle(error)
