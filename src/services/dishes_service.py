from uuid import UUID

from fastapi import BackgroundTasks, Depends
from starlette.responses import JSONResponse

from src.api.request_models.request_base import DishRequest
from src.api.response_models.dish_response import DishResponse
from src.repositories.dishes_repository import DishRepository
from src.services.cache_service import CacheService


class DishService:
    """Service for working with model Dish."""

    def __init__(
        self,
        background_tasks: BackgroundTasks,
        dish_repository: DishRepository = Depends(),
        cache_service: CacheService = Depends(),
    ) -> None:
        self.__background_tasks = background_tasks
        self._dish_repository = dish_repository
        self._cache_service = cache_service

    async def create_dish(
        self, menu_id: UUID, submenu_id: UUID, schema: DishRequest
    ) -> DishResponse:
        """Service function for creation object dish and saving cache."""
        dish = await self._dish_repository.create_dish_db(submenu_id, schema)
        await self._cache_service.set_cache(
            f'menu_id-{menu_id}:submenu_id-{submenu_id}:dish_id-{dish.id}',
            dish,
        )
        self.__background_tasks.add_task(
            self._cache_service.delete_caches,
            [
                f'submenus_list_{menu_id}',
                f'dishes_list_{menu_id}_{submenu_id}',
                'all_menus'
            ],
        )
        return dish

    async def update_dish(
        self,
        menu_id: UUID,
        submenu_id: UUID,
        dish_id: UUID,
        schema: DishRequest,
    ) -> DishResponse:
        """Service function for updating object dish and saving cache."""
        dish = await self._dish_repository.update_dish_db(dish_id, schema)
        await self._cache_service.set_cache(
            f'menu_id-{menu_id}:submenu_id-{submenu_id}:dish_id-{dish.id}',
            dish,
        )
        self.__background_tasks.add_task(
            self._cache_service.delete_caches,
            [f'dishes_list_{menu_id}_{submenu_id}', 'all_menus'],
        )
        return dish

    async def get_dish(
        self, menu_id: UUID, submenu_id: UUID, dish_id: UUID
    ) -> DishResponse:
        """Service function for get object dish from DB or redis cache."""
        cached_dish = await self._cache_service.get_cache(
            f'menu_id-{menu_id}:submenu_id-{submenu_id}:dish_id-{dish_id}'
        )
        if cached_dish:
            return cached_dish
        dish = await self._dish_repository.get_dish_db(dish_id)
        await self._cache_service.set_cache(dish_id, dish)
        return dish

    async def delete_dish(
        self, menu_id: UUID, submenu_id: UUID, dish_id: UUID
    ) -> JSONResponse:
        """Service function for delete object dish from DB and redis cache."""
        self.__background_tasks.add_task(
            self._cache_service.delete_caches,
            [
                f'menu_id-{menu_id}:submenu_id-{submenu_id}:dish_id-{dish_id}',
                f'dishes_list_{menu_id}_{submenu_id}',
                'all_menus'
            ],
        )
        self.__background_tasks.add_task(
            self._cache_service.invalidate_cache_for_submenu,
            menu_id,
            submenu_id,
        )
        delete_dish_from_db = await self._dish_repository.delete_dish_db(
            dish_id
        )
        return delete_dish_from_db

    async def get_dishes(
        self, menu_id: UUID, submenu_id: UUID
    ) -> list[DishResponse]:
        """Service function for get list of dishes from DB or redis cache."""
        cache_key = f'dishes_list_{menu_id}_{submenu_id}'
        cached_dishes = await self._cache_service.get_cache(cache_key)

        if cached_dishes:
            return cached_dishes
        dishes_response = await self._dish_repository.get_list_of_dishes_db(
            menu_id, submenu_id
        )
        await self._cache_service.set_cache(cache_key, dishes_response)
        return dishes_response
