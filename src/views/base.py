import contextlib
from typing import Generator

from flask.views import MethodView

from src.services import BaseService
from src.utils.types import ServiceType
from wsgi import app


class BaseView(MethodView):
    @contextlib.contextmanager
    def _get_service(self, service: type[BaseService]) -> Generator[ServiceType, None, None]:
        with app.database.session() as session:
            yield service(session)

    @property
    def _service(self):
        raise NotImplementedError
