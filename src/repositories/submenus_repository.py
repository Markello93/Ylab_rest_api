from typing import List, Optional
from uuid import UUID

from fastapi import Depends
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.request_models.request_base import MenuRequest
from src.api.response_models.submenu_response import SubmenuInfoResponse
from src.core import exceptions
from src.db.db import get_session
from src.db.models import Menu, Submenu
from src.repositories.abstract_repository import AbstractRepository


class SubmenuRepository(AbstractRepository):
    """Repository associated with model Submenu."""

    def __init__(self, session: AsyncSession = Depends(get_session)):
        super().__init__(session, Submenu)

    async def get_list_of_submenus_db(
        self, menu_id: UUID
    ) -> List[SubmenuInfoResponse]:
        """Get all submenus for menu with quantity of dishes from database."""
        stmt = (
            select(Submenu, func.count(Submenu.dishes).label("dishes_count"))
            .join(Submenu.dishes, isouter=True)
            .where(Submenu.menu_id == menu_id)
            .group_by(Submenu)
        )
        submenus_with_counts = (await self._session.execute(stmt)).all()

        submenu_responses = [
            SubmenuInfoResponse(
                id=submenu.id,
                title=submenu.title,
                description=submenu.description,
                menu_id=submenu.menu_id,
                dishes_count=dishes_count,
            )
            for submenu, dishes_count in submenus_with_counts
        ]

        return submenu_responses

    async def get_submenu_db(self, submenu_id: UUID) -> Submenu:
        """Get submenu by submenu_id."""
        return await self.get(submenu_id)

    async def get_submenu_with_count_db(
        self, submenu_id: UUID
    ) -> Optional[SubmenuInfoResponse]:
        """ "Get submenu with count of dishes from database."""
        stmt = (
            select(Submenu, func.count(Submenu.dishes).label("dishes_count"))
            .join(Submenu.dishes, isouter=True)
            .where(Submenu.id == submenu_id)
            .group_by(Submenu)
        )
        submenu_with_counts = (await self._session.execute(stmt)).first()

        if submenu_with_counts:
            submenu, dishes_count = submenu_with_counts
            response = SubmenuInfoResponse(
                id=submenu.id,
                title=submenu.title,
                description=submenu.description,
                menu_id=submenu.menu_id,
                dishes_count=dishes_count,
            )
            return response

        raise exceptions.ObjectNotFoundError("submenu not found")

    async def create_submenu_db(
        self, menu_id: UUID, schema: MenuRequest
    ) -> Submenu:
        """Create submenu object in the database."""
        menu = await self._session.get(Menu, menu_id)
        if menu is None:
            raise exceptions.ObjectNotFoundError("Menu not found")
        submenu = Submenu(
            title=schema.title, description=schema.description, menu_id=menu_id
        )
        return await self.create(submenu)

    async def update_submenu_db(
        self, submenu_id: UUID, schema: MenuRequest
    ) -> Submenu:
        """Update submenu object in the database with the provided data."""
        submenu = await self.get_submenu_db(submenu_id)
        submenu.title = schema.title
        submenu.description = schema.description
        return await self.update(submenu)

    async def delete_submenu_db(self, submenu_id: UUID) -> None:
        """Delete submenu object from the database."""
        submenu = await self.get_submenu_db(submenu_id)
        await self.delete(submenu.id)
