from functools import cache

from pydantic import BaseSettings


class Settings(BaseSettings):
    """Project settings."""

    DEBUG: bool = False
    RESTO_ROOT_PATH: str = ''
    RESTO_APP_DB_NAME: str
    RESTO_APP_DB_USER: str
    RESTO_APP_DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    DB_HOST_TEST: str
    DB_PORT_TEST: int
    DB_NAME_TEST: str
    DB_USER_TEST: str
    DB_PASS_TEST: str
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_DB: int
    REDIS_CACHE_LIFETIME: int

    @property
    def database_url(self) -> str:
        """Get link for DB connection."""
        return (
            f'postgresql+asyncpg://'
            f'{self.RESTO_APP_DB_USER}:{self.RESTO_APP_DB_PASSWORD}'
            f'@{self.DB_HOST}:{self.DB_PORT}/{self.RESTO_APP_DB_NAME}'
        )

    @property
    def database_test_url(self) -> str:
        """Get link for test DB connection."""
        return (
            f'postgresql+asyncpg://'
            f'{self.DB_USER_TEST}:{self.DB_PASS_TEST}'
            f'@{self.DB_HOST_TEST}:{self.DB_PORT_TEST}/{self.DB_NAME_TEST}'
        )

    @property
    def redis_url(self) -> str:
        """Get link for redis connection."""
        return (
            f'redis://{self.REDIS_HOST}:{self.REDIS_PORT}/0'
        )

    class Config:
        env_file = '.env'


@cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
