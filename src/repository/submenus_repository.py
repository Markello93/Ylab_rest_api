from typing import List
from uuid import UUID

from fastapi import Depends
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.db import get_session
from src.db.models import Dish, Submenu
from src.repository.abstract_repository import AbstractRepository


class SubmenuRepository(AbstractRepository):
    """Репозиторий для работы с моделью Submenu."""

    def __init__(self, session: AsyncSession = Depends(get_session)):
        super().__init__(session, Submenu)

    async def get_all_submenus_with_counts(self) -> List[Submenu]:
        submenus = await self.get_all()
        for submenu in submenus:
            submenu.dish_count = await self.get_dish_count_for_submenu(submenu.id)
        return submenus

    async def get_dish_count_for_submenu(self, submenu_id: UUID) -> int:
        stmt = select(func.count()).where(Dish.submenu_id == submenu_id)
        dishes_available = await self._session.scalar(stmt)
        return await dishes_available or 0
