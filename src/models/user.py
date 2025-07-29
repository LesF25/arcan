from typing import Optional

from sqlalchemy import String, Integer, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.schema import ForeignKey

from .base import BaseModel


class UserModel(BaseModel):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    login: Mapped[str] = mapped_column(
        String,
        unique=True,
        nullable=False,
    )
    password: Mapped[str] = mapped_column(
        String,
        deferred=True,
        nullable=False,
    )
    status: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )
    full_name: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )
    email: Mapped[str] = mapped_column(
        String,
        unique=True,
        nullable=False,
    )
    phone_number: Mapped[str] = mapped_column(
        String(12),
        unique=True,
        nullable=False,
    )

    # FOREIGN KEYS
    client_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey('clients.id'),
    )
    role_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('roles.id'),
        nullable=False,
    )

    # RELATIONSHIPS
    client: Mapped['ClientModel'] = relationship(
        back_populates='user'
    )
    event: Mapped['EventModel'] = relationship(
        back_populates='user'
    )
    user_session: Mapped['UserSessionModel'] = relationship(
        back_populates='user',
        cascade='all, delete-orphan'
    )
    role: Mapped['RoleModel'] = relationship(
        back_populates='users',
    )
