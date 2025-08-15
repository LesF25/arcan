import settings


class BaseConfig:
    DATABASE_URI = None
    REDIS_URI = None


class TestConfig(BaseConfig):
    DATABASE_URI = settings.TEST_DATABASE_URI
    REDIS_URI = settings.TEST_REDIS_URI
    TESTING = True


class Config(BaseConfig):
    DATABASE_URI = settings.DATABASE_URI
    REDIS_URI = settings.REDIS_URI
