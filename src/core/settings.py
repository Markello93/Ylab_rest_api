import os
from functools import cache

from pydantic import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    """Настройки проекта."""

    DEBUG: bool = False
    RESTO_ROOT_PATH: str = ""
    RESTO_APP_DB_NAME: str #= os.getenv('RESTO_APP_DB_NAME')
    RESTO_APP_DB_USER: str #= os.getenv('RESTO_APP_DB_USER')
    RESTO_APP_DB_PASSWORD: str #= os.getenv('RESTO_APP_DB_PASSWORD')
    DB_HOST: str #= os.getenv('DB_HOST')
    DB_PORT: int #= os.getenv('DB_PORT')

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
