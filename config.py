import settings


class BaseConfig:
    DATABASE_URI = None


class TestConfig(BaseConfig):
    DATABASE_URI = settings.TEST_DATABASE_URI
    TESTING = True


class Config(BaseConfig):
    DATABASE_URI = settings.DATABASE_URI
