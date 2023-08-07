from redis import asyncio as aioredis
from redis.asyncio.connection import ConnectionPool
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from src.core.settings import settings

engine = create_async_engine(settings.database_url, future=True, echo=False)
SessionLocal = sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)


async def get_session() -> AsyncSession:
    async with SessionLocal() as session:
        yield session


# async def create_redis():
#     """Создание соединение с Redis."""
#     return ConnectionPool.from_url(settings.redis_url)
#
# pool = await create_redis()
#
#
# async def get_redis():
#     """Возвращает соединение с Redis."""
#     return aioredis.Redis(connection_pool=pool)


class RedisConnection:
    def __init__(self, redis_url):
        self.redis_url = redis_url
        self.pool = None

    async def __aenter__(self):
        self.pool = ConnectionPool.from_url(self.redis_url)
        return aioredis.Redis(connection_pool=self.pool)

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.pool.disconnect()


async def create_redis_connection(redis_url=settings.redis_url):
    """Создание соединения с Redis."""
    async with RedisConnection(redis_url) as redis_conn:
        yield redis_conn
