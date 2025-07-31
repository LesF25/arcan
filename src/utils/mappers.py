from sqlalchemy.orm import MappedColumn

from src.models import UserModel, RoleModel, ClientModel


class BaseMapper:
    MAP_COLUMNS = {}

    @classmethod
    def get_column(cls, field_name) -> MappedColumn:
        return cls.MAP_COLUMNS[field_name]


class UserMapper(BaseMapper):
    MAP_COLUMNS = {
        'id': UserModel.id,
        'login': UserModel.login,
        'status': UserModel.status,
        'role_name': RoleModel.name,
        'client_name': ClientModel.name,
    }
