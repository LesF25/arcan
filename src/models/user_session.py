from datetime import datetime, timedelta

from sqlalchemy import String, Integer, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.schema import ForeignKey

from .base import BaseModel


class UserSessionModel(BaseModel):
    __tablename__ = 'user_sessions'

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )
    token: Mapped[int] = mapped_column(
        String,
        unique=True,
        nullable=False,
    )
    expired: Mapped[datetime] = mapped_column(
        DateTime,
        default=(
            datetime.now() + timedelta(days=7)
        ),
        nullable=False,
    )

    # FOREIGN KEYS
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('users.id'),
        nullable=False,
    )

    # RELATIONSHIPS
    user: Mapped['UserModel'] = relationship(
        back_populates='user_session',
    )
