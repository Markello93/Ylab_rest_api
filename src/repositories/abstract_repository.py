import abc
from typing import Optional, TypeVar
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.core import exceptions
from src.db.models import Dish, Menu, Submenu

DatabaseModel = TypeVar("DatabaseModel")


class AbstractRepository(abc.ABC):
    """Abstract class for Repository pattern implementation."""

    ERROR_MESSAGES = {
        Menu: "menu not found",
        Submenu: "submenu not found",
        Dish: "dish not found",
    }

    def __init__(self, session: AsyncSession, model: DatabaseModel) -> None:
        self._session = session
        self._model = model

    async def create(self, instance: DatabaseModel) -> DatabaseModel:
        self._session.add(instance)
        try:
            await self._session.commit()
        except IntegrityError:
            await self._session.rollback()
            raise exceptions.ObjectAlreadyExistsError(instance)

        return instance

    async def get_or_none(self, instance_id: UUID) -> Optional[DatabaseModel]:
        db_obj = await self._session.execute(
            select(self._model).where(self._model.id == instance_id)
        )
        return db_obj.scalars().first()

    async def get(self, instance_id: UUID) -> DatabaseModel:
        """Get object by ID. Raise error if object not found."""
        stmt = select(self._model).where(self._model.id == instance_id)
        db_obj = (await self._session.execute(stmt)).scalars().first()
        if db_obj is None:
            error_message = self.ERROR_MESSAGES.get(
                self._model, "Object not found"
            )
            raise exceptions.ObjectNotFoundError(error_message)
        return db_obj

    async def get_all(self) -> list[DatabaseModel]:
        """Return all objects from database."""
        objects = await self._session.execute(select(self._model))
        return objects.scalars().all()

    async def update(self, instance: DatabaseModel) -> DatabaseModel:
        existing_instance = await self._session.get(self._model, instance.id)
        if existing_instance is None:
            error_message = self.ERROR_MESSAGES.get(
                self._model, "Object not found"
            )
            raise exceptions.ObjectNotFoundError(error_message)
        instance = await self._session.merge(instance)
        await self._session.commit()
        return instance

    async def delete(self, instance_id: UUID) -> None:
        db_obj = await self.get(instance_id)
        if db_obj is None:
            error_message = self.ERROR_MESSAGES.get(
                self._model, "Object not found"
            )
            raise exceptions.ObjectNotFoundError(error_message)
        await self._session.delete(db_obj)
        await self._session.commit()
