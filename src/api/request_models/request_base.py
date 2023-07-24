from pydantic import BaseModel


class MenuRequest(BaseModel):
    title: str
    description: str


class DishRequest(BaseModel):
    title: str
    description: str
    price: str
