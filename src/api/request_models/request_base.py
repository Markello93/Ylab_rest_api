from decimal import Decimal

from pydantic import BaseModel, Field


class MenuRequest(BaseModel):
    """Request model for submenus and menus."""

    title: str
    description: str


class DishRequest(BaseModel):
    """Request model for dishes."""

    title: str
    description: str
    price: Decimal = Field(max_digits=10, decimal_places=2)
