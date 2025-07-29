from sqlalchemy import ForeignKey, UniqueConstraint, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import BaseModel


class LicensePurchaseModel(BaseModel):
    __tablename__ = 'license_purchases'

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    device_count: Mapped[int] = mapped_column(
        Integer,
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
    component: Mapped['ComponentModel'] = relationship(
        back_populates='license_purchase',
    )
    client: Mapped['ClientModel'] = relationship(
        back_populates='license_purchase',
    )
    license_type: Mapped['LicenseType'] = relationship(
        back_populates='license_purchases',
    )

    __table_args__ = (
        UniqueConstraint(
            columns=[
                'client_id',
                'component_id',
                'license_type_id',
            ],
            name='__constraint_license_purchases'
        ),
    )
