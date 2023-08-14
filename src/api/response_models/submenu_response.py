from pydantic import UUID4, BaseModel

from src.api.response_models.dish_response import DishMenusResponse


class SubmenuResponse(BaseModel):
    """Response model for submenu without count of dishes."""

    id: UUID4
    title: str
    description: str

    class Config:
        orm_mode = True


class SubmenuInfoResponse(SubmenuResponse):
    """Response model for submenu with count of dishes."""

    menu_id: UUID4
    dishes_count: int | None = 0

    class Config:
        orm_mode = True


class SubmenusSummaryResponse(SubmenuResponse):
    """Response model for submenu with count of dishes."""

    dishes: list[DishMenusResponse]

    class Config:
        orm_mode = True
