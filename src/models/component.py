from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import BaseModel


class ComponentModel(BaseModel):
    __tablename__ = 'components'

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    name: Mapped[str] = mapped_column(
        String(25),
        nullable=False,
    )
    module_rsa_pub: Mapped[str] = mapped_column(
        String,
        unique=True,
        deferred=True,
        nullable=True
    )
    server_rsa_pub: Mapped[str] = mapped_column(
        String,
        unique=True,
        deferred=True,
        nullable=True,
    )
    server_rsa_private: Mapped[str] = mapped_column(
        String,
        unique=True,
        deferred=True,
        nullable=True,
    )

    # RELATIONSHIPS
    license_purchase: Mapped['LicensePurchasesModel'] = relationship(
        back_populates='component',
    )
    license_request: Mapped['LicenseRequestModel'] = relationship(
        back_populates='component',
    )
