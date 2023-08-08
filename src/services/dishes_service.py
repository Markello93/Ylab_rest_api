from uuid import UUID

from fastapi import Depends

from src.api.request_models.request_base import DishRequest
from src.db.models import Dish
from src.repositories.dishes_repository import DishRepository
from src.services.cache_service import CacheService


class DishService:
    """Service for working with model Dish."""

    def __init__(
        self,
        dish_repository: DishRepository = Depends(),
        cache_service: CacheService = Depends(),
    ) -> None:
        self._dish_repository = dish_repository
        self._cache_service = cache_service

    async def create_dish(
        self, menu_id: UUID, submenu_id: UUID, schema: DishRequest
    ) -> Dish:
        """Service function for creation object dish and saving cache."""
        dish = await self._dish_repository.create_dish_db(submenu_id, schema)
        await self._cache_service.set_cache(
            f'menu_id-{menu_id}:submenu_id-{submenu_id}:dish_id-{dish.id}',
            dish,
        )
        await self._cache_service.delete_cache(
            f'dishes_list_{menu_id}_{submenu_id}'
        )
        return dish

    async def update_dish(
        self,
        menu_id: UUID,
        submenu_id: UUID,
        dish_id: UUID,
        schema: DishRequest,
    ) -> Dish:
        """Service function for updating object dish and saving cache."""
        dish = await self._dish_repository.update_dish_db(dish_id, schema)
        await self._cache_service.set_cache(
            f'menu_id-{menu_id}:submenu_id-{submenu_id}:dish_id-{dish.id}',
            dish,
        )
        await self._cache_service.delete_cache(
            f'dishes_list_{menu_id}_{submenu_id}'
        )
        return dish

    async def get_dish(
        self, menu_id: UUID, submenu_id: UUID, dish_id: UUID
    ) -> Dish:
        """Service function for get object dish from DB or redis cache."""
        cached_dish = await self._cache_service.get_cache(
            f'menu_id-{menu_id}:submenu_id-{submenu_id}:dish_id-{dish_id}'
        )
        if cached_dish is None:
            dish = await self._dish_repository.get_dish_db(dish_id)
            await self._cache_service.set_cache(dish_id, dish)
            return dish
        return cached_dish

    async def delete_dish(self, menu_id, submenu_id, dish_id: UUID) -> None:
        """Service function for delete object dish from DB and redis cache."""
        await self._cache_service.delete_cache(
            f'menu_id-{menu_id}:submenu_id-{submenu_id}:dish_id-{dish_id}'
        )
        await self._cache_service.invalidate_cache_for_submenu(menu_id, submenu_id)
        await self._cache_service.delete_cache(
            f'dishes_list_{menu_id}_{submenu_id}'
        )
        await self._dish_repository.delete_dish_db(dish_id)

    async def get_dishes(
        self, menu_id: UUID, submenu_id: UUID
    ) -> list[Dish]:
        """Service function for get list of dishes from DB or redis cache."""
        cache_key = f'dishes_list_{menu_id}_{submenu_id}'
        cached_dishes = await self._cache_service.get_cache(cache_key)

        if cached_dishes is None:
            dishes_response = (
                await self._dish_repository.get_list_of_dishes_db(
                    menu_id, submenu_id
                )
            )
            await self._cache_service.set_cache(cache_key, dishes_response)
            return dishes_response
        return cached_dishes
