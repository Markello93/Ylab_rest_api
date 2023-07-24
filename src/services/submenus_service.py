from uuid import UUID

from fastapi import Depends

from src.api.request_models.request_base import MenuRequest
from src.api.response_models.submenu_response import AllSubmenuResponse
from src.db.models import Submenu
from src.repositories.submenus_repository import SubmenuRepository


class SubmenuService:
    def __init__(
        self,
        submenus_repository: SubmenuRepository = Depends(),
    ) -> None:
        self._submenus_repository = submenus_repository

    async def list_all_submenus(self) -> list[AllSubmenuResponse]:
        return await self._submenus_repository.get_all_submenus_with_counts()

    async def create_submenu(
        self, menu_id: UUID, schema: MenuRequest
    ) -> Submenu:
        return await self._submenus_repository.create_submenu(menu_id, schema)

    async def update_submenu(
        self, menu_id: UUID, submenu_id: UUID, schema: MenuRequest
    ) -> Submenu:
        return await self._submenus_repository.update_submenu(
            menu_id, submenu_id, schema
        )

    async def get_submenu(self, menu_id: UUID, submenu_id: UUID) -> Submenu:
        return await self._submenus_repository.get_submenu(menu_id, submenu_id)

    async def delete_submenu(self, menu_id: UUID, submenu_id: UUID):
        await self._submenus_repository.delete_submenu(menu_id, submenu_id)
