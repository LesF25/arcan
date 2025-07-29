from flask import Flask

import settings
from config import Config
from application.structures import Rule
from src.views import rules
from src.models import BaseModel
from .db import SQLAlchemyDB


class Application(Flask):
    def __init__(
        self,
        import_name: str,
        database: SQLAlchemyDB,
    ):
        super().__init__(import_name)
        self.config.from_object(Config)
        self.database = database

    def add_rules(
        self,
        rules: list[Rule],
    ) -> None:
        for rule in rules:
            self.add_url_rule(**rule.as_dict())


app = Application(
    __name__,
    database=SQLAlchemyDB(
        db_uri=settings.DATABASE_URI,
        base_model=BaseModel,
    ),
)
app.add_rules(rules)
