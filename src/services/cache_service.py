import pickle
from typing import Any

from redis import asyncio as aioredis
from redis.asyncio.connection import ConnectionPool

from src.core.settings import settings


class CacheService:
    def __init__(self):
        self.redis_url: str = settings.redis_url
        self.lifetime: int = settings.REDIS_CACHE_LIFETIME

    async def get_redis_connection(self):
        pool = ConnectionPool.from_url(self.redis_url)
        return await aioredis.Redis(connection_pool=pool)

    async def set_cache(self, key: str, value: Any) -> None:
        value = pickle.dumps(value)
        redis_conn = await self.get_redis_connection()
        try:
            await redis_conn.set(key, value, ex=self.lifetime)
        finally:
            await redis_conn.close()

    async def get_cache(self, key: str) -> Any:
        redis_conn = await self.get_redis_connection()
        try:
            cache = await redis_conn.get(key)
            if cache:
                return pickle.loads(cache)
            return None
        finally:
            await redis_conn.close()

    async def delete_cache(self, key: str) -> None:
        redis_conn = await self.get_redis_connection()
        try:
            await redis_conn.delete(key)
        finally:
            await redis_conn.close()

    async def flush_redis(self) -> None:
        """Очистка всего кэша."""
        redis_conn = await self.get_redis_connection()
        try:
            await redis_conn.flushdb()
        finally:
            await redis_conn.close()
