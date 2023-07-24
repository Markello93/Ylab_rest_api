from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from typing import List
from uuid import UUID

from src.api.request_models.request_base import MenuRequest
from src.api.response_models.menu_response import AllMenuResponse
from src.db.models import Menu
from src.db.db import get_session
from src.repositories.abstract_repository import AbstractRepository


class MenuRepository(AbstractRepository):
    def __init__(self, session: AsyncSession = Depends(get_session)):
        super().__init__(session, Menu)

    async def get_menu(self, menu_id: UUID) -> Menu:
        """Get menu by menu_id. Raise exception if not found."""
        return await self.get(menu_id)

    async def get_all_menus_with_counts(self) -> List[AllMenuResponse]:
        menus = await self.get_all()
        menu_responses = []
        for menu in menus:
            menu_response = AllMenuResponse(
                id=menu.id,
                title=menu.title,
                description=menu.description,
                submenus_count=menu.num_submenus,
                dishes_count=menu.num_dishes,
            )
            menu_responses.append(menu_response)
        return menu_responses

    async def create_menu(self, schema: MenuRequest) -> Menu:
        menu = Menu(title=schema.title, description=schema.description)
        return await self.create(menu)

    async def update_menu(self, menu_id: UUID, schema: MenuRequest) -> Menu:
        menu = await self.get_menu(menu_id)
        menu.title = schema.title
        menu.description = schema.description

        return await self.update(menu)

    async def delete_menu(self, menu_id: UUID) -> None:
        menu = await self.get_menu(menu_id)
        await self.delete(menu.id)
