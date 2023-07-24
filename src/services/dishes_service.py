from typing import List
from uuid import UUID

from fastapi import Depends

from src.api.request_models.request_base import DishRequest
from src.db.models import Dish

from src.repositories.dishes_repository import DishRepository


class DishService:
    def __init__(
        self,
        dish_repository: DishRepository = Depends(),
    ) -> None:
        self._dish_repository = dish_repository

    async def create_dish(
        self, menu_id: UUID, submenu_id: UUID, schema: DishRequest
    ) -> Dish:
        return await self._dish_repository.create_dish(
            menu_id, submenu_id, schema
        )

    async def update_dish(
        self,
        menu_id: UUID,
        submenu_id: UUID,
        dish_id: UUID,
        schema: DishRequest,
    ) -> Dish:
        return await self._dish_repository.update_dish(
            menu_id, submenu_id, dish_id, schema
        )

    async def get_dish(
        self, menu_id: UUID, submenu_id: UUID, dish_id: UUID
    ) -> Dish:
        return await self._dish_repository.get_dish(
            menu_id, submenu_id, dish_id
        )

    async def delete_dish(
        self, menu_id: UUID, submenu_id: UUID, dish_id: UUID
    ):
        await self._dish_repository.delete_dish(menu_id, submenu_id, dish_id)

    async def list_all_dishes(
        self, menu_id: UUID, submenu_id: UUID
    ) -> List[Dish]:
        return await self._dish_repository.get_dishes(menu_id, submenu_id)
