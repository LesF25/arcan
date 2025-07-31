import pytest
from flask import Response
from sqlalchemy.exc import SQLAlchemyError

from src.error_handler import (
    add_error_handler,
    get_handler_by_error,
    BaseErrorHandler,
    DefaultErrorHandler,
)


class TestError(Exception):
    ...


@add_error_handler(TestError)
class TestErrorHandler(BaseErrorHandler):
    def handle(
        self,
        error: Exception,
    ) -> Response:
        ...


@pytest.mark.parametrize('exception, expected_handler', [
    (TestError(), TestErrorHandler),            # exists
    (SQLAlchemyError(), DefaultErrorHandler),   # default
])
def test_error_handler(
    exception: Exception,
    expected_handler: BaseErrorHandler,
) -> None:
    error_handler = get_handler_by_error(exception)
    assert type(error_handler) is expected_handler
