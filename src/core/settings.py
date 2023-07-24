from functools import cache

from pydantic import BaseSettings


class Settings(BaseSettings):
    """Настройки проекта."""

    DEBUG: bool = False
    RESTO_ROOT_PATH: str = ""
    RESTO_APP_DB_NAME: str
    RESTO_APP_DB_USER: str
    RESTO_APP_DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int

    @property
    def database_url(self) -> str:
        """Получить ссылку для подключения к DB."""
        return (
            f"postgresql+asyncpg://"
            f"{self.RESTO_APP_DB_USER}:{self.RESTO_APP_DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.RESTO_APP_DB_NAME}"
        )

    class Config:
        env_file = ".env"


@cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
