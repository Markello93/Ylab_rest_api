from uuid import UUID

from fastapi import Depends

from src.api.request_models.request_base import MenuRequest
from src.api.response_models.submenu_response import SubmenuInfoResponse
from src.db.models import Submenu
from src.repositories.submenus_repository import SubmenuRepository


class SubmenuService:
    """Service for working with model Submenu."""

    def __init__(
        self,
        submenus_repository: SubmenuRepository = Depends(),
    ) -> None:
        self._submenus_repository = submenus_repository

    async def create_submenu(
        self, menu_id: UUID, schema: MenuRequest
    ) -> Submenu:
        return await self._submenus_repository.create_submenu_db(
            menu_id, schema
        )

    async def update_submenu(
        self, submenu_id: UUID, schema: MenuRequest
    ) -> Submenu:
        return await self._submenus_repository.update_submenu_db(
            submenu_id, schema
        )

    async def get_submenu(self, submenu_id: UUID) -> SubmenuInfoResponse:
        return await self._submenus_repository.get_submenu_with_count_db(
            submenu_id
        )

    async def delete_submenu(self, submenu_id: UUID):
        await self._submenus_repository.delete_submenu_db(submenu_id)

    async def list_all_submenus(
        self, menu_id: UUID
    ) -> list[SubmenuInfoResponse]:
        return await self._submenus_repository.get_list_of_submenus_db(menu_id)
