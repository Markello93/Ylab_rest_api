from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from src.core.settings import settings

engine = create_async_engine(settings.database_url, future=True, echo=False)
SessionLocal = sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)


async def get_session() -> AsyncSession:
    """Creation connection to Db."""
    async with SessionLocal() as session:
        yield session
