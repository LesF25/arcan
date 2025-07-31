import pytest
from flask import Response
from flask.testing import FlaskClient
from sqlalchemy.exc import SQLAlchemyError

from src.exception import DeleteError
from src.utils import json_helpers


@pytest.mark.parametrize('exception, error_message, expected_response', [
    (
        ValueError,
        'ValueError message.',
        Response(
            response=json_helpers.dumps({
                'message': (
                    'Your request contains invalid data. '
                    'Please check the provided details.'
                ),
                'detail': 'ValueError message.',
            }),
            status=400,
        ),
    ),
    (
        DeleteError,
        'DeleteError message.',
        Response(
            response=json_helpers.dumps({
                'success': False,
                'message': (
                    "Couldn't delete the resource. "
                    'Please try again or contact support if the issue persists.'
                ),
                'detail': 'DeleteError message.',
            }),
            status=500
        ),
    ),
    (
        SQLAlchemyError,
        'SQLAlchemyError message.',
        Response(
            response=json_helpers.dumps({
                'message': 'Something went wrong. Please contact Sinthy Support.',
                'detail': 'SQLAlchemyError message.',
            }),
            status=500,
        ),
    ),
])
def test_error_handler(
    f_client: FlaskClient,
    exception: type[Exception],
    error_message: str,
    expected_response: Response,
) -> None:
    f_client.application.config['TEST_EXCEPTION_TO_RAISE'] = {
        'class': exception,
        'message': error_message,
    }

    response = f_client.get('/test-error-handler')

    assert response.text == response.text
    assert response.status_code == response.status_code
