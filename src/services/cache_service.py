import functools
import pickle
from typing import Union

from pydantic import UUID4
from redis import asyncio as aioredis
from redis.asyncio.connection import ConnectionPool

from src.api.response_models.dish_response import DishResponse
from src.api.response_models.menu_response import MenuInfResponse, MenuSummaryResponse
from src.api.response_models.submenu_response import SubmenuInfoResponse
from src.core.settings import settings

CacheResponseType = Union[
    DishResponse,
    MenuInfResponse,
    SubmenuInfoResponse,
    list[DishResponse],
    list[MenuInfResponse],
    list[SubmenuInfoResponse],
    list[MenuSummaryResponse],
    None,
]


def with_redis_connection(func):
    @functools.wraps(func)
    async def wrapper(self, *args, **kwargs) -> CacheResponseType:
        redis_conn = await self.get_redis_connection()
        try:
            return await func(self, redis_conn, *args, **kwargs)
        finally:
            await redis_conn.close()

    return wrapper


class CacheService:
    def __init__(self) -> None:
        self.redis_url: str = settings.redis_url
        self.lifetime: int = settings.REDIS_CACHE_LIFETIME

    async def get_redis_connection(self) -> aioredis.Redis | None:
        """Get connection for Redis DB"""
        pool = ConnectionPool.from_url(self.redis_url)
        return await aioredis.Redis(connection_pool=pool)

    @with_redis_connection
    async def set_cache(
        self, redis_conn: aioredis.Redis, key: str, value: bytes
    ) -> None:
        """Set cache for object in redis DB."""
        value = pickle.dumps(value)
        await redis_conn.set(key, value, ex=self.lifetime)

    @with_redis_connection
    async def get_cache(
        self, redis_conn: aioredis.Redis, key: str
    ) -> CacheResponseType:
        """Get cache for object in redis DB."""
        cache = await redis_conn.get(key)
        if cache:
            return pickle.loads(cache)
        return None

    @with_redis_connection
    async def delete_caches(
        self, redis_conn: aioredis.Redis, keys: list
    ) -> None:
        """Delete multiple caches for given keys."""
        await redis_conn.delete(*keys)

    @with_redis_connection
    async def invalidate_cache_for_menu(
        self, redis_conn: aioredis.Redis, menu_id: UUID4
    ) -> None:
        """Delete cache for menu and all related submenus and dishes."""
        keys = await redis_conn.keys(f'menu_id-{menu_id}*')
        if keys:
            await redis_conn.delete(*keys)

    @with_redis_connection
    async def invalidate_cache_for_submenu(
        self, redis_conn: aioredis.Redis, menu_id: UUID4, submenu_id: UUID4
    ) -> None:
        """Delete cache for submenu and all related dishes."""
        keys = await redis_conn.keys(
            f'menu_id-{menu_id}:submenu_id-{submenu_id}*'
        )
        if keys:
            await redis_conn.delete(*keys)

    @with_redis_connection
    async def flush_redis(self, redis_conn: aioredis.Redis) -> None:
        """Clear all cache."""
        await redis_conn.flushdb()
