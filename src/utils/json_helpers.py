import datetime
import json

import pydantic

from src.models import *
from src.schemas import *


class CustomJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, pydantic.BaseModel):
            return obj.model_dump()

        if isinstance(obj, datetime.datetime):
            ...

        return super().default(obj)


def dumps(response: dict) -> str:
    return json.dumps(response, cls=CustomJsonEncoder)
