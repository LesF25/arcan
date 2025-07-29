from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import BaseModel


class LicenseTypeModel(BaseModel):
    __tablename__ = 'license_types'

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    name: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )

    # RELATIONSHIPS
    license_requests: Mapped[list['LicenseRequestModel']] = relationship(
        back_populates='license_type',
        uselist=False,
    )
    license_purchases: Mapped[list['LicensePurchaseModel']] = relationship(
        back_populates='license_type',
        uselist=False,
    )
