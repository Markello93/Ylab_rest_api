from pydantic import BaseModel


class MenuRequest(BaseModel):
    """Request model for submenus and menus."""

    title: str
    description: str


class DishRequest(BaseModel):
    """Request model for dishes."""

    title: str
    description: str
    price: str
