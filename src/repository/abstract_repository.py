import abc
from typing import Optional, TypeVar
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.core import exceptions

DatabaseModel = TypeVar("DatabaseModel")


class AbstractRepository(abc.ABC):
    """Abstract class for Repository pattern implementation."""

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
            raise exceptions.ObjectNotFoundError(self._model)
        return db_obj

    async def get_all(self) -> list[DatabaseModel]:
        """Return all objects from database."""
        objects = await self._session.execute(select(self._model))
        return objects.scalars().all()

    async def update(self, instance: DatabaseModel) -> DatabaseModel:
        existing_instance = await self._session.get(self._model, instance.id)
        if existing_instance is None:
            raise exceptions.ObjectNotFoundError(self._model)

        instance = await self._session.merge(instance)
        await self._session.commit()
        return instance

    async def delete(self, instance_id: UUID) -> None:
        db_obj = await self.get(instance_id)
        await self._session.delete(db_obj)
        await self._session.commit()

