from datetime import datetime, timedelta
from typing import Optional

from sqlalchemy.sql.sqltypes import (
    Integer,
    String,
    BigInteger,
    Boolean,
    DateTime,
)
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
)
from sqlalchemy.schema import ForeignKey, UniqueConstraint


class BaseModel(DeclarativeBase):
    ...


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
            *[
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
        ForeignKey('users.id'),
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
            *[
                'client_id',
                'component_id',
                'license_type_id',
            ],
            name='__constraint_license_purchases'
        ),
    )


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


class RoleModel(BaseModel):
    __tablename__ = 'roles'

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    name: Mapped[int] = mapped_column(
        String,
        nullable=False,
    )

    # RELATIONSHIPS
    users: Mapped[list['UserModel']] = relationship(
        back_populates='role',
        uselist=False,
    )


class UserModel(BaseModel):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    login: Mapped[str] = mapped_column(
        String,
        unique=True,
        nullable=False,
    )
    password: Mapped[str] = mapped_column(
        String,
        deferred=True,
        nullable=False,
    )
    status: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
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

    # FOREIGN KEYS
    client_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey('clients.id'),
    )
    role_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('roles.id'),
        nullable=False,
    )

    # RELATIONSHIPS
    client: Mapped['ClientModel'] = relationship(
        back_populates='user'
    )
    event: Mapped['EventModel'] = relationship(
        back_populates='user'
    )
    user_session: Mapped['UserSessionModel'] = relationship(
        back_populates='user',
        cascade='all, delete-orphan'
    )
    role: Mapped['RoleModel'] = relationship(
        back_populates='users',
    )


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
