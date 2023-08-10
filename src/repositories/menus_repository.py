from uuid import UUID

from fastapi import Depends
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse

from src.api.request_models.request_base import MenuRequest
from src.api.response_models.menu_response import MenuInfResponse
from src.core import exceptions
from src.db.db import get_session
from src.db.models import Dish, Menu, Submenu
from src.repositories.abstract_repository import AbstractRepository


class MenuRepository(AbstractRepository):
    """Repository associated with model Menu."""

    def __init__(self, session: AsyncSession = Depends(get_session)) -> None:
        super().__init__(session, Menu)

    async def get_menu_db(self, menu_id: UUID) -> Menu:
        """Get menu by menu_id."""
        return await self.get_instance(menu_id)

    async def get_menu_db_with_counts(self, menu_id: UUID) -> MenuInfResponse:
        """Get menu by menu_id with submenu and dish counts."""
        stmt = (
            select(
                Menu,
                func.count(Submenu.id.distinct()).label('submenus_count'),
                func.count(Dish.id.distinct()).label('dishes_count'),
            )
            .outerjoin(Submenu, Menu.submenus)
            .outerjoin(Dish, Submenu.dishes)
            .where(Menu.id == menu_id)
            .group_by(Menu.id)
        )
        menu_with_counts = (await self._session.execute(stmt)).first()

        if menu_with_counts:
            menu, submenus_count, dishes_count = menu_with_counts
            menu_response = MenuInfResponse(
                id=menu.id,
                title=menu.title,
                description=menu.description,
                submenus_count=submenus_count,
                dishes_count=dishes_count,
            )
            return menu_response

        raise exceptions.ObjectNotFoundError('menu not found')

    async def get_list_of_menus_db(self) -> list[MenuInfResponse]:
        """Get list of menus with quantity of submenus and dishes."""
        stmt = (
            select(
                Menu,
                func.count(Submenu.id).label('submenus_count'),
                func.count(Dish.id).label('dishes_count'),
            )
            .join(Menu.submenus, isouter=True)
            .join(Submenu.dishes, isouter=True)
            .group_by(Menu.id)
        )
        menus_with_counts = await self._session.execute(stmt)

        menu_responses = []
        for menu, submenus_count, dishes_count in menus_with_counts:
            menu_response = MenuInfResponse(
                id=menu.id,
                title=menu.title,
                description=menu.description,
                submenus_count=submenus_count,
                dishes_count=dishes_count,
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

    async def delete_menu_db(self, menu_id: UUID) -> JSONResponse:
        """Delete menu object from the database."""
        menu = await self.get_menu_db(menu_id)
        await self.delete(menu.id)
        return JSONResponse(
            status_code=200,
            content={
                'message': 'The menu was successfully removed from the database'
            },
        )
