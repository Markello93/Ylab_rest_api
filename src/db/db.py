from typing import AsyncGenerator

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
    """Creation connection to Db."""
    async with SessionLocal() as session:
        yield session


class RedisConnection:
    """Class for establishing a connection to Redis."""

    def __init__(self, redis_url):
        self.redis_url = redis_url
        self.pool = None

    async def __aenter__(self) -> aioredis.Redis:
        """Establishes a connection to Redis and returns an aioredis.Redis object."""
        self.pool = ConnectionPool.from_url(self.redis_url)
        return aioredis.Redis(connection_pool=self.pool)

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Disconnects from Redis when exiting the context."""
        await self.pool.disconnect()


async def create_redis_connection(redis_url: str = settings.redis_url) -> AsyncGenerator[aioredis.Redis, None]:
    """Creation connection with Redis."""
    async with RedisConnection(redis_url) as redis_conn:
        yield redis_conn
