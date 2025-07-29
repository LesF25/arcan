from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import BaseModel


class EventTypeModel(BaseModel):
    __tablename__ = 'event_types'

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    name: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    # RELATIONSHIPS
    events: Mapped[list['EventModel']] = relationship(
        back_populates='event_type',
        uselist=False,
    )
