from uuid import UUID

from fastapi import Depends

from src.api.request_models.request_base import MenuRequest
from src.api.response_models.submenu_response import SubmenuInfoResponse
from src.repositories.submenus_repository import SubmenuRepository
from src.services.cache_service import CacheService


class SubmenuService:
    """Service for working with model Submenu."""

    def __init__(
        self,
        submenus_repository: SubmenuRepository = Depends(),
            cache_service: CacheService = Depends(),
    ) -> None:
        self._submenus_repository = submenus_repository
        self._cache_service = cache_service

    async def create_submenu(
        self, menu_id: UUID, schema: MenuRequest
    ) -> SubmenuInfoResponse:
        submenu = await self._submenus_repository.create_submenu_db(
            menu_id, schema
        )
        await self._cache_service.set_cache(str(submenu.id), submenu)
        return submenu

    async def update_submenu(
        self, submenu_id: UUID, schema: MenuRequest
    ) -> SubmenuInfoResponse:

        submenu = await self._submenus_repository.update_submenu_db(
            submenu_id, schema
        )
        await self._cache_service.set_cache(str(submenu.id), submenu)
        return submenu

    async def get_submenu(self, submenu_id: UUID) -> SubmenuInfoResponse:
        cached_submenu = await self._cache_service.get_cache(str(submenu_id))
        if cached_submenu is None or not hasattr(cached_submenu, 'dishes_count'):
            submenu = await self._submenus_repository.get_submenu_with_count_db(
                submenu_id
            )
            await self._cache_service.set_cache(str(submenu_id), submenu)
            return submenu
        return cached_submenu

    async def delete_submenu(self, menu_id: UUID, submenu_id: UUID):
        await self._cache_service.delete_cache(str(menu_id))
        await self._cache_service.delete_cache(str(submenu_id))
        await self._submenus_repository.delete_submenu_db(submenu_id)

    async def list_all_submenus(self, menu_id: UUID) -> list[
            SubmenuInfoResponse]:
        cache_key = f'submenus_list_{menu_id}'
        cached_submenus = await self._cache_service.get_cache(cache_key)

        if cached_submenus is None:
            submenus_response = await self._submenus_repository.get_list_of_submenus_db(
                menu_id)
            await self._cache_service.set_cache(cache_key, submenus_response)
            return submenus_response

        # Если кеш не пустой, проверяем, обновлены ли данные в базе данных
        # Если да, обновляем кеш и возвращаем новый результат
        updated_submenus = await self._submenus_repository.get_list_of_submenus_db(
            menu_id)
        if cached_submenus != updated_submenus:
            await self._cache_service.set_cache(cache_key, updated_submenus)

        return updated_submenus
