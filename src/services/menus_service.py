from uuid import UUID

from fastapi import Depends

from src.api.request_models.request_base import MenuRequest
from src.db.models import Menu

from src.repositories.menus_repository import MenuRepository


class MenuService:
    """Service for working with model Menu."""

    def __init__(
        self,
        menu_repository: MenuRepository = Depends(),
    ) -> None:
        self._menu_repository = menu_repository

    async def create_menu(self, schema: MenuRequest) -> Menu:
        return await self._menu_repository.create_menu_db(schema)

    async def update_menu(self, menu_id: UUID, schema: MenuRequest) -> Menu:
        return await self._menu_repository.update_menu_db(menu_id, schema)

    async def get_menu(self, menu_id: UUID) -> Menu:
        return await self._menu_repository.get_menu_db(menu_id)

    async def delete_menu(self, menu_id: UUID):
        await self._menu_repository.delete_menu_db(menu_id)

    async def get_menus(self):
        return await self._menu_repository.get_list_of_menus_db()
