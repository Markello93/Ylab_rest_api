import abc
from typing import Generic, TypeVar

from pydantic import UUID4
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.core import exceptions
from src.db.models import Dish, Menu, Submenu


class HasID:
    __abstract__ = True
    id: UUID4


DatabaseModel = TypeVar('DatabaseModel', bound='HasID')


class AbstractRepository(Generic[DatabaseModel], abc.ABC):
    """
    Abstract class for Repository pattern implementation, include all
    CRUD operations.
    """

    ERROR_MESSAGES = {
        Menu: 'menu not found',
        Submenu: 'submenu not found',
        Dish: 'dish not found',
    }

    def __init__(self, session: AsyncSession, model: type[DatabaseModel]) -> None:
        self._session = session
        self._model = model

    async def create(self, instance: DatabaseModel) -> DatabaseModel:
        """
        Create object in the database. Raise error if object already
        exist.
        """
        self._session.add(instance)
        try:
            await self._session.commit()
        except IntegrityError:
            await self._session.rollback()
            raise exceptions.ObjectAlreadyExistsError(instance)

        return instance

    async def get_or_none(self, instance_id: UUID4) -> DatabaseModel | None:
        """Get object by ID. Return None if object not found."""
        db_obj: DatabaseModel | None = await self._session.execute(
            select(self._model).where(self._model.id == instance_id)
        ).scalars().first()
        return db_obj

    async def get_instance(self, instance_id: UUID4) -> DatabaseModel:
        """Get object by ID. Raise error if object not found."""
        stmt = select(self._model).where(self._model.id == instance_id)
        db_obj: DatabaseModel | None = (await self._session.execute(stmt)).scalars().first()
        if db_obj is None:
            error_message = self.ERROR_MESSAGES.get(
                self._model, 'Object not found'
            )
            raise exceptions.ObjectNotFoundError(error_message)
        return db_obj

    async def get_all(self) -> list[DatabaseModel]:
        """Return all objects from database."""
        objects = await self._session.execute(select(self._model))
        return objects.scalars().all()

    async def update(self, instance: DatabaseModel) -> DatabaseModel:
        """Update object by ID. Raise error if object not found."""
        existing_instance = await self._session.get(self._model, instance.id)
        if existing_instance is None:
            error_message = self.ERROR_MESSAGES.get(
                self._model, 'Object not found'
            )
            raise exceptions.ObjectNotFoundError(error_message)
        instance = await self._session.merge(instance)
        await self._session.commit()
        return instance

    async def delete(self, instance_id: UUID4) -> None:
        """Delete object by ID. Raise error if object not found."""
        db_obj: DatabaseModel | None = await self.get_instance(instance_id)
        if db_obj is None:
            error_message = self.ERROR_MESSAGES.get(
                self._model, 'Object not found'
            )
            raise exceptions.ObjectNotFoundError(error_message)
        await self._session.delete(db_obj)
        await self._session.commit()
        return None
