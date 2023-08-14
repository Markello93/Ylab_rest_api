import uuid
from decimal import Decimal

import sqlalchemy as sa
from sqlalchemy import Numeric, UniqueConstraint
from sqlalchemy.dialects.postgresql import TEXT, UUID
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(AsyncAttrs, DeclarativeBase):
    """Base class for database models with UUID-based primary key."""

    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        default=uuid.uuid4,
        primary_key=True,
    )

    def __repr__(self):
        return f'{self.__class__.__name__}(id={self.id})'


class Menu(Base):
    """Model for creating Menu object in the database."""

    __tablename__ = 'menus'

    title: Mapped[str] = mapped_column(TEXT, nullable=False, unique=True)
    description: Mapped[str] = mapped_column(TEXT, nullable=False)
    submenus: Mapped[list['Submenu']] = relationship(
        'Submenu',
        back_populates='menu',
        cascade='all, delete-orphan',
        lazy='selectin',
    )


class Submenu(Base):
    """Model for creating Submenu object in the database."""

    __tablename__ = 'submenus'

    title: Mapped[str] = mapped_column(TEXT, nullable=False, unique=True)
    description: Mapped[str] = mapped_column(TEXT, nullable=False)
    menu_id: Mapped[UUID | None] = mapped_column(
        sa.ForeignKey('menus.id'), nullable=False
    )
    menu: Mapped['Menu'] = relationship(
        'Menu', back_populates='submenus', lazy='selectin'
    )

    dishes: Mapped[list['Dish']] = relationship(
        'Dish',
        back_populates='submenu',
        cascade='all, delete-orphan',
        lazy='selectin',
    )

    __table_args__ = (UniqueConstraint('title', 'menu_id'),)


class Dish(Base):
    """Model for creating Dish object in the database."""

    __tablename__ = 'dishes'

    title: Mapped[str] = mapped_column(TEXT, nullable=False, unique=True)
    description: Mapped[str] = mapped_column(TEXT, nullable=False)
    price: Mapped[Decimal | None] = mapped_column(
        Numeric(precision=7, scale=2), nullable=False
    )
    submenu_id: Mapped[UUID | None] = mapped_column(
        sa.ForeignKey('submenus.id'), nullable=False
    )
    submenu: Mapped['Submenu'] = relationship(
        'Submenu', back_populates='dishes', lazy='selectin'
    )
