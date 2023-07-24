from sqlalchemy import select

from src.api.request_models.request_base import DishRequest

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from typing import List, Optional
from uuid import UUID

from src.db.models import Dish, Menu, Submenu
from src.db.db import get_session
from src.repositories.abstract_repository import AbstractRepository


class DishRepository(AbstractRepository):
    """Репозиторий для работы с моделью Dish."""

    def __init__(self, session: AsyncSession = Depends(get_session)):
        super().__init__(session, Dish)

    async def get_dish(
        self, menu_id: UUID, submenu_id: UUID, dish_id: UUID
    ) -> Dish:
        """Get dish by id."""

        return await self.get(dish_id)

    async def get_dishes(
        self, menu_id: UUID, submenu_id: UUID
    ) -> List[Optional[Dish]]:
        stmt = (
            select(Dish)
            .join(Submenu)
            .join(Menu)
            .where(
                Submenu.id == submenu_id,
                Menu.id == menu_id,
            )
        )

        dishes = await self._session.execute(stmt)
        return dishes.scalars().all()

    async def update_dish(
        self,
        menu_id: UUID,
        submenu_id: UUID,
        dish_id: UUID,
        schema: DishRequest,
    ) -> Dish:
        dish = await self.get_dish(menu_id, submenu_id, dish_id)
        dish.title = schema.title
        dish.description = schema.description
        dish.price = schema.price
        return await self.update(dish)

    async def delete_dish(
        self, menu_id: UUID, submenu_id: UUID, dish_id: UUID
    ) -> None:
        dish = await self.get_dish(menu_id, submenu_id, dish_id)
        await self.delete(dish.id)

    async def create_dish(
        self, menu_id: UUID, submenu_id: UUID, schema: DishRequest
    ) -> Dish:
        dish = Dish(
            title=schema.title,
            description=schema.description,
            price=schema.price,
            submenu_id=submenu_id,
        )
        return await self.create(dish)
