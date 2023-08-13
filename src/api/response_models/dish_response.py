from decimal import Decimal

from pydantic import UUID4, BaseModel


class DishResponse(BaseModel):
    """Response model for Dish."""

    id: UUID4
    title: str
    description: str
    price: Decimal
    submenu_id: UUID4

    class Config:
        orm_mode = True
        json_encoders = {Decimal: lambda v: str(v)}


class DishMenusResponse(BaseModel):
    """Response model for Dish."""

    id: UUID4
    title: str
    description: str
    price: Decimal

    class Config:
        orm_mode = True
        json_encoders = {Decimal: lambda v: str(v)}
