import uuid
from decimal import Decimal
from typing import List, Optional

from sqlalchemy import Numeric, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID, TEXT
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import relationship
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
import sqlalchemy as sa


class Base(AsyncAttrs, DeclarativeBase):
    """Base class for database models with UUID-based primary key."""

    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        default=uuid.uuid4,
        primary_key=True,
    )

    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.id})"


class Menu(Base):
    """Model for creating Menu object in the database."""

    __tablename__ = "menus"

    title: Mapped[str] = mapped_column(TEXT, nullable=False, unique=True)
    description: Mapped[str] = mapped_column(TEXT, nullable=False)
    submenus: Mapped[List["Submenu"]] = relationship(
        "Submenu",
        back_populates="menu",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    @property
    def num_submenus(self):
        return len(self.submenus)

    @property
    def num_dishes(self):
        return sum(submenu.num_dishes for submenu in self.submenus)


class Submenu(Base):
    """Model for creating Submenu object in the database."""

    __tablename__ = "submenus"

    title: Mapped[str] = mapped_column(TEXT, nullable=False, unique=True)
    description: Mapped[str] = mapped_column(TEXT, nullable=False)
    menu_id: Mapped[Optional[UUID]] = mapped_column(
        sa.ForeignKey("menus.id"), nullable=False
    )
    menu: Mapped["Menu"] = relationship(
        "Menu", back_populates="submenus", lazy="selectin"
    )

    dishes: Mapped[List["Dish"]] = relationship(
        "Dish",
        back_populates="submenu",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    __table_args__ = (UniqueConstraint("title", "menu_id"),)

    @property
    def num_dishes(self):
        return len(self.dishes)


class Dish(Base):
    """Model for creating Dish object in the database."""

    __tablename__ = "dishes"

    title: Mapped[str] = mapped_column(TEXT, nullable=False, unique=True)
    description: Mapped[str] = mapped_column(TEXT, nullable=False)
    price: Mapped[Optional[Decimal]] = mapped_column(
        Numeric(precision=5, scale=2), nullable=False
    )
    submenu_id: Mapped[Optional[UUID]] = mapped_column(
        sa.ForeignKey("submenus.id"), nullable=False
    )
    submenu: Mapped["Submenu"] = relationship(
        "Submenu", back_populates="dishes", lazy="selectin"
    )
