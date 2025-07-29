from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import BaseModel


class RoleModel(BaseModel):
    __tablename__ = 'roles'
    
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    name: Mapped[int] = mapped_column(
        String,
        nullable=False,
    )

    # RELATIONSHIPS
    users: Mapped[list['UserModel']] = relationship(
        back_populates='role',
        uselist=False,
    )
