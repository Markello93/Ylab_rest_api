from uuid import UUID

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.request_models.request_base import DishRequest
from src.core import exceptions
from src.db.db import get_session
from src.db.models import Dish, Menu, Submenu
from src.repositories.abstract_repository import AbstractRepository


class DishRepository(AbstractRepository):
    """Repository associated with model Dish."""

    def __init__(self, session: AsyncSession = Depends(get_session)):
        super().__init__(session, Dish)

    async def get_dish_db(self, dish_id: UUID) -> Dish:
        """Get dish by dish_id."""
        return await self.get_instance(dish_id)

    async def get_list_of_dishes_db(
        self, menu_id: UUID, submenu_id: UUID
    ) -> list[Dish | None]:
        """Get all dishes for submenu."""
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

    async def create_dish_db(
        self, submenu_id: UUID, schema: DishRequest
    ) -> Dish:
        """Create dish object in the database."""
        submenu = await self._session.get(Submenu, submenu_id)
        if submenu is None:
            raise exceptions.ObjectNotFoundError('submenu not found')
        dish = Dish(
            title=schema.title,
            description=schema.description,
            price=schema.price,
            submenu_id=submenu_id,
        )
        return await self.create(dish)

    async def update_dish_db(
        self,
        dish_id: UUID,
        schema: DishRequest,
    ) -> Dish:
        """Update dish object in the database with the provided data."""
        dish = await self.get_dish_db(dish_id)
        dish.title = schema.title
        dish.description = schema.description
        dish.price = schema.price
        return await self.update(dish)

    async def delete_dish_db(self, dish_id: UUID) -> None:
        """Delete dish object from the database."""
        dish = await self.get_dish_db(dish_id)
        await self.delete(dish.id)
