from pydantic import BaseModel, UUID4


class AllMenuResponse(BaseModel):
    id: UUID4
    title: str
    description: str
    submenus_count: int
    dishes_count: int

    class Config:
        orm_mode = True


class MenuResponse(BaseModel):
    id: UUID4
    title: str
    description: str

    class Config:
        orm_mode = True


class Menu_with_infoResponse(BaseModel):
    id: UUID4
    title: str
    description: str
    submenus_count: int
    dishes_count: int

    class Config:
        orm_mode = True
