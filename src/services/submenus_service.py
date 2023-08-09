from uuid import UUID

from fastapi import Depends
from starlette.responses import JSONResponse

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
        """Service function for creation object submenu and saving cache."""
        submenu = await self._submenus_repository.create_submenu_db(
            menu_id, schema
        )
        await self._cache_service.set_cache(
            f'menu_id-{menu_id}:submenu_id-{submenu.id}', submenu
        )
        await self._cache_service.delete_caches([f'submenus_list_{menu_id}'])
        return submenu

    async def update_submenu(
        self, submenu_id: UUID, schema: MenuRequest
    ) -> SubmenuInfoResponse:
        """Service function for update object submenu and saving cache."""
        submenu = await self._submenus_repository.update_submenu_db(
            submenu_id, schema
        )
        await self._cache_service.set_cache(
            f'menu_id-{submenu.menu_id}:submenu_id-{submenu.id}', submenu
        )
        await self._cache_service.delete_caches(
            [f'submenus_list_{submenu.menu_id}']
        )
        return submenu

    async def get_submenu(
        self, menu_id: UUID, submenu_id: UUID
    ) -> SubmenuInfoResponse:
        """Service function for get object submenu from DB or redis cache."""
        cached_submenu = await self._cache_service.get_cache(
            f'menu_id-{menu_id}:submenu_id-{submenu_id}'
        )
        if cached_submenu is None or not hasattr(
            cached_submenu, 'dishes_count'
        ):
            submenu = (
                await self._submenus_repository.get_submenu_with_count_db(
                    submenu_id
                )
            )
            await self._cache_service.set_cache(
                f'menu_id-{submenu.menu_id}:submenu_id-{submenu.id}', submenu
            )
            return submenu
        return cached_submenu

    async def delete_submenu(
        self, menu_id: UUID, submenu_id: UUID
    ) -> JSONResponse:
        """Service function for delete object submenu from DB and redis cache."""
        await self._cache_service.invalidate_cache_for_menu(menu_id)
        await self._cache_service.delete_caches([f'submenus_list_{menu_id}'])
        delete_submenu_from_db = (
            await self._submenus_repository.delete_submenu_db(submenu_id)
        )
        return delete_submenu_from_db

    async def get_submenus(self, menu_id: UUID) -> list[SubmenuInfoResponse]:
        """Service function for get list of submenus from DB or redis cache."""
        cache_key = f'submenus_list_{menu_id}'
        cached_submenus = await self._cache_service.get_cache(cache_key)

        if cached_submenus is None:
            submenus_response = (
                await self._submenus_repository.get_list_of_submenus_db(
                    menu_id
                )
            )
            await self._cache_service.set_cache(cache_key, submenus_response)
            return submenus_response
        return cached_submenus
