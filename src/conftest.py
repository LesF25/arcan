import pytest
from flask import current_app
from flask.testing import FlaskClient

from config import TestConfig
from src import Application
from src.structures import Rule


def __test_error_handler():
    exception_info = current_app.config.get('TEST_EXCEPTION_TO_RAISE')
    exception = exception_info['class']

    raise exception(exception_info['message'])


rules = [
    Rule(
        rule='/test-error-handler',
        view_func=__test_error_handler,
        methods=['GET'],
    ),
]


@pytest.fixture(scope='session')
def f_client() -> FlaskClient:
    app = Application.init(
        config=TestConfig,
        rules=rules
    )
    app.testing = True

    with app.test_client() as client:
        yield client
