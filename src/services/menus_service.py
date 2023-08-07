from uuid import UUID

from fastapi import Depends

from src.api.request_models.request_base import MenuRequest
from src.api.response_models.menu_response import MenuInfResponse
from src.repositories.menus_repository import MenuRepository
from src.services.cache_service import CacheService


class MenuService:
    """Service for working with model Menu."""

    def __init__(
            self,
            menu_repository: MenuRepository = Depends(),
            cache_service: CacheService = Depends(),
    ) -> None:
        self._menu_repository = menu_repository
        self._cache_service = cache_service

    async def create_menu(self, schema: MenuRequest) -> MenuInfResponse:
        menu = await self._menu_repository.create_menu_db(schema)
        await self._cache_service.set_cache(str(menu.id), menu)
        return menu

    async def update_menu(self, menu_id: UUID, schema: MenuRequest) -> MenuInfResponse:
        menu = await self._menu_repository.update_menu_db(menu_id, schema)
        await self._cache_service.set_cache(str(menu.id), menu)
        return menu

    async def get_menu(self, menu_id: UUID) -> MenuInfResponse:
        cached_menu = await self._cache_service.get_cache(str(menu_id))
        if cached_menu is None or not hasattr(cached_menu, 'submenus_count'):
            menu_response = await self._menu_repository.get_menu_db_with_counts(menu_id)
            await self._cache_service.set_cache(str(menu_id), menu_response)
            return menu_response
        return cached_menu

    async def delete_menu(self, menu_id: UUID):
        await self._cache_service.delete_cache(str(menu_id))
        await self._menu_repository.delete_menu_db(menu_id)

    async def get_menus(self):
        cached_menus = await self._cache_service.get_cache('list_menus')

        if cached_menus is None:
            menus_response = await self._menu_repository.get_list_of_menus_db()
            await self._cache_service.set_cache('list_menus', menus_response)
            return menus_response
        updated_menus = await self._menu_repository.get_list_of_menus_db()
        if cached_menus != updated_menus:
            await self._cache_service.set_cache('list_menus', updated_menus)

        return updated_menus
