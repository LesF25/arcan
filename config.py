from sqlalchemy.engine import URL, make_url

import settings


class Config:
    DATABASE_URI = settings.DATABASE_URI
