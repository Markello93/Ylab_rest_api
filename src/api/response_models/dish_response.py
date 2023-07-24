from decimal import Decimal
from pydantic import BaseModel, UUID4


class DishResponse(BaseModel):
    id: UUID4
    title: str
    description: str
    price: Decimal
    submenu_id: UUID4

    class Config:
        orm_mode = True
        json_encoders = {Decimal: lambda v: str(v)}
