from pydantic import BaseModel, UUID4


class AllSubmenuResponse(BaseModel):
    """Response model for submenu with count of dishes."""

    id: UUID4
    title: str
    description: str
    menu_id: UUID4
    dishes_count: int

    class Config:
        orm_mode = True


class SubmenuResponse(BaseModel):
    """Response model for submenu without count of dishes."""

    id: UUID4
    title: str
    description: str
    menu_id: UUID4

    class Config:
        orm_mode = True
