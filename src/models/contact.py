from sqlalchemy import ForeignKey, Integer, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import BaseModel


class ContactModel(BaseModel):
    __tablename__ = 'contacts'

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
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
    post: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )
    description: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )
    turn_on_notification: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
    )

    # FOREIGN KEYS
    client_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('clients.id'),
        nullable=False,
    )

    # RELATIONSHIPS
    client: Mapped['ClientModel'] = relationship(
        back_populates='contact',
    )
