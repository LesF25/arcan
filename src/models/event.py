from datetime import datetime
from typing import Optional

from sqlalchemy import ForeignKey, Integer, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import BaseModel


class EventModel(BaseModel):
    __tablename__ = 'events'

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    date_event: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now(),
        nullable=False,
    )

    # FOREIGN KEYS
    user_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey('user.id'),
    )
    event_type_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('event_types.id'),
        nullable=False
    )
    license_request_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey('license_requests.id')
    )

    # RELATIONSHIPS
    user: Mapped['UserModel'] = relationship(
        back_populates='event',
    )
    license_request: Mapped['LicenseRequestModel'] = relationship(
        back_populates='event',
    )
    event_type: Mapped['EventTypeModel'] = relationship(
        back_populates='events',
    )
