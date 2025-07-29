from flask.views import MethodView

from ..services.base import BaseService


class BaseView(MethodView):
    def __init__(
        self,
        service: BaseService,
    ) -> None:
        self._service = service
        super().__init__()
