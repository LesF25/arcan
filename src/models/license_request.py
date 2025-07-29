from datetime import datetime

from sqlalchemy import ForeignKey, Integer, DateTime, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import BaseModel


class LicenseRequestModel(BaseModel):
    __tablename__ = 'license_requests'

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    license_expiration_date: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
    )
    technical_support_expiration_date: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
    )
    request_creation_mode: Mapped[str] = mapped_column(
        String,
        default='auto',
        nullable=False,
    )
    is_license_issued: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    # FOREIGN KEYS
    license_type_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('license_types.id'),
        nullable=False,
    )
    component_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('components.id'),
        nullable=False,
    )
    client_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('clients.id'),
        nullable=False,
    )

    # RELATIONSHIPS
    license_type: Mapped['LicenseTypeModel'] = relationship(
        back_populates='license_requests',
    )
    component: Mapped['ComponentModel'] = relationship(
        back_populates='license_request',
    )
    client: Mapped['ClientModel'] = relationship(
        back_populates='license_request'
    )
    event: Mapped['EventModel'] = relationship(
        back_populates='license_request',
        cascade='all, delete-orphan',
    )
    network_adapter: Mapped['NetworkAdapterModel'] = relationship(
        back_populates='license_request',
        cascade='all, delete-orphan',
    )
