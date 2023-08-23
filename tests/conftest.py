import asyncio
import os
import sys
from asyncio import AbstractEventLoop
from typing import AsyncGenerator, Generator

import pytest
from faker import Faker
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from run import app
from src.core.settings import Settings, get_settings, settings
from src.db.db import get_session
from src.db.models import Base

sys.path.append(os.path.join(os.getcwd(), 'src'))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
fake = Faker()
engine_test = create_async_engine(settings.database_test_url, echo=False)
async_session_maker = sessionmaker(
    engine_test, class_=AsyncSession, expire_on_commit=False
)
Base.metadata.bind = engine_test


async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


app.dependency_overrides[get_session] = override_get_async_session


@pytest.fixture(scope='session', autouse=True)
async def prepare_database() -> AsyncGenerator:
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def clear_db():
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@pytest.fixture(scope='session')
def event_loop(request) -> Generator[AbstractEventLoop, None, None]:
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope='session')
def app_settings() -> Settings:
    return get_settings()


@pytest.fixture(scope='session')
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(
        app=app, base_url='http://tests', follow_redirects=True
    ) as ac:
        yield ac


@pytest.fixture
def menu_data() -> dict:
    """Fixture for fake menus and submenus."""
    return {'title': fake.sentence(), 'description': fake.sentence()}


@pytest.fixture
def dish_data() -> dict:
    """Fixture for fake dishes."""
    return {
        'title': fake.sentence(),
        'description': fake.sentence(),
        'price': str(
            fake.pydecimal(left_digits=3, right_digits=2, positive=True)
        ),
    }


@pytest.fixture(scope='class')
async def created_menu(ac: AsyncClient) -> dict:
    menu_data = {'title': fake.sentence(), 'description': fake.sentence()}
    response = await ac.post('/api/v1/menus/', json=menu_data)
    return response.json()


@pytest.fixture(scope='class')
async def created_submenu(ac: AsyncClient) -> dict:
    menu_data = {'title': fake.sentence(), 'description': fake.sentence()}
    response = await ac.post('/api/v1/menus/', json=menu_data)
    respone_json = response.json()
    submenu_data = {'title': fake.sentence(), 'description': fake.sentence()}
    response = await ac.post(
        f"/api/v1/menus/{respone_json['id']}/submenus/", json=submenu_data
    )
    return response.json()


@pytest.fixture(scope='class')
async def created_dish(
    ac: AsyncClient, created_menu: dict, created_submenu: dict
) -> dict:
    dish_data = {
        'title': fake.sentence(),
        'description': fake.sentence(),
        'price': str(
            fake.pydecimal(left_digits=3, right_digits=2, positive=True)
        ),
    }
    response = await ac.post(
        f"/api/v1/menus/{created_menu['id']}/submenus/{created_submenu['id']}/dishes/",
        json=dish_data,
    )
    return response.json()


@pytest.fixture(scope='session')
async def submenu_created_info() -> dict:
    """Fixture for saving ids during tests"""
    return {}


@pytest.fixture(scope='session')
async def dish_created_info() -> dict:
    """Fixture for saving ids during tests"""
    return {}


@pytest.fixture(scope='session')
async def menu_created_info() -> dict:
    """Fixture for saving ids during tests"""
    return {}
