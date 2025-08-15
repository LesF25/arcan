import os

# ex: postgresql://postgres:m3t8L1iE@localhost:5432/postgres
DATABASE_URI = os.getenv('DATABASE_URI')
TEST_DATABASE_URI = os.getenv('TEST_DATABASE_URI')

# ex: redis://[[username]:[password]]@localhost:6379/0
REDIS_URI = os.getenv('REDIS_URI')

SECRET_KEY = os.getenv('SECRET_KEY')  # for gen credentials
