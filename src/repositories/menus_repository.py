from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from typing import List
from uuid import UUID

from src.api.request_models.request_base import MenuRequest
from src.api.response_models.menu_response import MenuInfResponse
from src.db.models import Menu
from src.db.db import get_session
from src.repositories.abstract_repository import AbstractRepository


class MenuRepository(AbstractRepository):
    """Repository associated with model Menu."""

    def __init__(self, session: AsyncSession = Depends(get_session)):
        super().__init__(session, Menu)

    async def get_menu_db(self, menu_id: UUID) -> Menu:
        """Get menu by menu_id."""
        return await self.get(menu_id)

    async def get_list_of_menus_db(self) -> List[MenuInfResponse]:
        """Get list of menus with quantity of submenus and dishes."""
        menus = await self.get_all()
        menu_responses = []
        for menu in menus:
            menu_response = MenuInfResponse(
                id=menu.id,
                title=menu.title,
                description=menu.description,
                submenus_count=menu.num_submenus,
                dishes_count=menu.num_dishes,
            )
            menu_responses.append(menu_response)
        return menu_responses

    async def create_menu_db(self, schema: MenuRequest) -> Menu:
        """Create menu object in the database."""
        menu = Menu(title=schema.title, description=schema.description)
        return await self.create(menu)

    async def update_menu_db(self, menu_id: UUID, schema: MenuRequest) -> Menu:
        """Update menu object in the database with the provided data."""
        menu = await self.get_menu_db(menu_id)
        menu.title = schema.title
        menu.description = schema.description

        return await self.update(menu)

    async def delete_menu_db(self, menu_id: UUID) -> None:
        """Delete menu object from the database."""
        menu = await self.get_menu_db(menu_id)
        await self.delete(menu.id)
