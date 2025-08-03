from typing import Optional

import structlog
from flask import Flask, Response
from sqlalchemy import make_url

from config import BaseConfig
from .error_handler import get_handler_by_error
from .structures import Rule
from .models import BaseModel
from .db import SQLAlchemyDB

logger = structlog.get_logger(__name__)


class Application(Flask):
    def __init__(
        self,
        import_name: str,
        database: SQLAlchemyDB,
        config: type[BaseConfig],
    ) -> None:
        super().__init__(import_name)
        self.config.from_object(config)
        self.database = database

    @classmethod
    def init(
        cls,
        config: type[BaseConfig],
        rules: list[Rule] = None,
    ) -> 'Application':
        db = SQLAlchemyDB(
            uri=make_url(config.DATABASE_URI),
            base_model=BaseModel,
        )

        instance = cls(
            import_name=__name__,
            database=db,
            config=config,
        )
        instance._register_error_handler()
        instance._add_url_rules(rules)

        return instance

    def _register_error_handler(self):
        @self.errorhandler(Exception)
        def handle_error(error: Exception) -> Response:
            logger.error(
                'Error',
                error_message=str(error),
                exc_info=True
            )
            error_handler = get_handler_by_error(error)

            return error_handler.handle(error)

    def _add_url_rules(
        self,
        rules: list[Rule],
    ) -> None:
        for rule in rules:
            self.add_url_rule(**rule.model_dump())
