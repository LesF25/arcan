from sqlalchemy import String, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import BaseModel


class NetworkAdapterModel(BaseModel):
    __tablename__ = 'network_adapters'

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    name: Mapped[str] = mapped_column(
        String(10),
        nullable=False,
    )
    mac_address: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    # FOREIGN KEYS
    license_request_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('license_requests.id'),
        nullable=False,
    )

    # RELATIONSHIPS
    license_request: Mapped['LicenseRequestModel'] = relationship(
        back_populates='network_adapter',
    )
