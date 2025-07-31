from typing import Type

from sqlalchemy.engine import create_engine, URL
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Session
from sqlalchemy.exc import SQLAlchemyError


class SQLAlchemyDB:
    def __init__(
        self,
        uri: URL,
        base_model: Type[DeclarativeBase],
    ) -> None:
        self._engine = create_engine(uri)
        self._session = sessionmaker(self._engine)

        base_model.metadata.create_all(self._engine)

    def session(self) -> Session:
        session = self._session()
        try:
            yield session
            session.commit()
        except SQLAlchemyError:
            session.rollback()
            raise
        finally:
            session.close()


# class MongoDB(BaseDB):
#     def __init__(
#         self,
#         db_uri: str,
#     ) -> None:
#         self._engine = MongoClient(db_uri)
#
#     def session(self) -> ClientSession:
#         session = self._engine.start_session()
#         try:
#             with session.start_transaction():
#                 yield session
#                 session.commit_transaction()
#         except OperationFailure as error:
#             session.abort_transaction()
#             raise error
#         finally:
#             session.end_session()
#
#     @cached_property
#     def database(self):
#         return self._engine.get_default_database()
