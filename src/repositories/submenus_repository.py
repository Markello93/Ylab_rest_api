from typing import List
from uuid import UUID

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.request_models.request_base import MenuRequest
from src.api.response_models.submenu_response import AllSubmenuResponse
from src.db.db import get_session
from src.db.models import Submenu
from src.repositories.abstract_repository import AbstractRepository


class SubmenuRepository(AbstractRepository):
    def __init__(self, session: AsyncSession = Depends(get_session)):
        super().__init__(session, Submenu)

    async def get_all_submenus_with_counts(self) -> List[AllSubmenuResponse]:
        submenus = await self.get_all()
        submenu_responses = []
        for submenu in submenus:
            submenu_response = AllSubmenuResponse(
                id=submenu.id,
                title=submenu.title,
                description=submenu.description,
                menu_id=submenu.menu_id,
                dishes_count=submenu.num_dishes,
            )
            submenu_responses.append(submenu_response)
        return submenu_responses

    async def get_submenu(self, menu_id: UUID, submenu_id: UUID) -> Submenu:
        """Get Submenu by id."""
        submenu = await self.get(submenu_id)
        return submenu

    async def update_submenu(
        self, menu_id: UUID, submenu_id: UUID, schema: MenuRequest
    ) -> Submenu:
        submenu = await self.get_submenu(menu_id, submenu_id)
        submenu.title = schema.title
        submenu.description = schema.description
        return await self.update(submenu)

    async def delete_submenu(self, menu_id: UUID, submenu_id: UUID) -> None:
        submenu = await self.get_submenu(menu_id, submenu_id)
        await self.delete(submenu.id)

    async def create_submenu(
        self, menu_id: UUID, schema: MenuRequest
    ) -> Submenu:
        submenu = Submenu(
            title=schema.title, description=schema.description, menu_id=menu_id
        )
        return await self.create(submenu)
