from pydantic import UUID4, BaseModel

from src.api.response_models.submenu_response import SubmenusSummaryResponse


class MenuResponse(BaseModel):
    """Response model for menu without count of submenus and dishes."""

    id: UUID4
    title: str
    description: str

    class Config:
        orm_mode = True


class MenuInfResponse(MenuResponse):
    """Response model for menu with count of submenus and dishes."""

    submenus_count: int | None = 0
    dishes_count: int | None = 0

    class Config:
        orm_mode = True


class MenuSummaryResponse(MenuResponse):
    submenus: list[SubmenusSummaryResponse]

    class Config:
        orm_mode = True
