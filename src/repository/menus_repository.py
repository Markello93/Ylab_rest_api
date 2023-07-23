from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy import func
from fastapi import Depends
from typing import List
from uuid import UUID

from src.db.models import Menu, Submenu
from src.db.db import get_session
from src.repository.abstract_repository import AbstractRepository


# class MenuRepository(AbstractRepository):
#     def __init__(self, session: AsyncSession = Depends(get_session)):
#         super().__init__(session, Menu)
#
#     async def get_all_menus_with_counts(self) -> List[Menu]:
#         menus = await self.get_all()
#         for menu in menus:
#             menu.submenu_count = await self.get_submenu_count_for_menu(menu.id)
#             menu.dish_count = await self.get_dish_count_for_menu(menu.id)
#         return menus
#
#     async def get_submenu_count_for_menu(self, menu_id: UUID) -> int:
#         stmt = select(func.count()).where(Submenu.menu_id == menu_id)
#         submenu_available = self._session.scalar(stmt)
#         return await submenu_available or 0
#
#     async def get_dish_count_for_menu(self, menu_id: UUID) -> int:
#         stmt = select(func.count()).join(Submenu).where(Submenu.menu_id == menu_id)
#         dishes_available = await self._session.scalar(stmt)
#         return await dishes_available or 0

class MenuRepository(AbstractRepository):
    def __init__(self, session: AsyncSession = Depends(get_session)):
        super().__init__(session, Menu)

    async def get_all_menus_with_counts(self) -> List[Menu]:
        menus = await self.get_all()
        for menu in menus:
            menu.submenu_count = len(menu.submenus)
            menu.dish_count = sum(submenu.num_dishes for submenu in menu.submenus)
        return menus

