from typing import Optional

from sqlalchemy import Integer, String, UniqueConstraint, BigInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import BaseModel


class ClientModel(BaseModel):
    __tablename__ = 'clients'

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    name: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )
    tax_number: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False,
    )
    tax_registration_reason_code: Mapped[Optional[int]] = mapped_column(
        BigInteger,
    )
    legal_address: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )
    actual_address: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )
    general_director: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )
    website: Mapped[Optional[str]] = mapped_column(
        String,
    )
    group_name: Mapped[Optional[str]] = mapped_column(
        String,
    )
    branch_name: Mapped[Optional[int]] = mapped_column(
        String,
    )

    # RELATIONSHIPS
    user: Mapped['UserModel'] = relationship(
        back_populates='client',
    )
    contact: Mapped['ContactModel'] = relationship(
        back_populates='client',
        cascade='all, delete-orphan',
    )
    license_purchase: Mapped['LicensePurchaseModel'] = relationship(
        back_populates='client',
    )
    license_request: Mapped['LicenseRequestModel'] = relationship(
        back_populates='client',
    )

    __table_args__ = (
        UniqueConstraint(
            columns=[
                'name',
                'tax_number',
                'tax_registration_reason_code',
                'legal_address',
                'actual_address',
                'group_name',
                'branch_name',
            ],
            name='_constraint_client',
        ),
    )
