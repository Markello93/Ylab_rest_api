from pydantic import BaseModel, UUID4


class MenuResponse(BaseModel):
    """Response model for menu without count of submenus and dishes."""

    id: UUID4
    title: str
    description: str

    class Config:
        orm_mode = True


class MenuInfResponse(BaseModel):
    """Response model for menu with count of submenus and dishes."""

    id: UUID4
    title: str
    description: str
    submenus_count: int
    dishes_count: int

    class Config:
        orm_mode = True
