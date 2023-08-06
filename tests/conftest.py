import asyncio
import os
import sys
from typing import AsyncGenerator

import pytest
from faker import Faker
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from run import app
from src.core.settings import get_settings, settings
from src.db.db import get_session
from src.db.models import Base, Dish, Menu, Submenu

sys.path.append(os.path.join(os.getcwd(), 'src'))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
fake = Faker()
engine_test = create_async_engine(settings.database_test_url, echo=False)
async_session_maker = sessionmaker(engine_test, class_=AsyncSession, expire_on_commit=False)
Base.metadata.bind = engine_test


async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
app.dependency_overrides[get_session] = override_get_async_session


@pytest.fixture(scope='session', autouse=True)
async def prepare_database():
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope='session')
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope='session')
def app_settings():
    return get_settings()


@pytest.fixture(scope='session')
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url='http://tests', follow_redirects=True) as ac:
        yield ac


@pytest.fixture(scope='function')
async def last_menu_data():
    """Получение последнего меню из БД."""
    async with async_session_maker() as session:
        last_menu_id_result = await session.execute(
            select(Menu.id).order_by(Menu.id.desc()).limit(1)
        )
        last_menu_id = str(last_menu_id_result.scalar())
        last_menu_data_result = await session.execute(
            select(Menu.description, Menu.title).filter(Menu.id == last_menu_id)
        )
        description, title = last_menu_data_result.one()

        return {'id': last_menu_id, 'description': description, 'title': title}


@pytest.fixture(scope='function')
async def last_submenu_data():
    """Получение последнего подменю из БД."""
    async with async_session_maker() as session:
        last_submenu_id_result = await session.execute(
            select(Submenu.id).order_by(Submenu.id.desc()).limit(1)
        )
        last_submenu_id = str(last_submenu_id_result.scalar())
        last_submenu_data_result = await session.execute(
            select(Submenu.description, Submenu.title).filter(
                Submenu.id == last_submenu_id
            )
        )
        description, title = last_submenu_data_result.one()

        return {'id': last_submenu_id, 'description': description, 'title': title}


@pytest.fixture(scope='function')
async def last_dish_data():
    """Получение последнего блюда из БД."""
    async with async_session_maker() as session:
        last_dish_id_result = await session.execute(
            select(Dish.id).order_by(Dish.id.desc()).limit(1)
        )
        last_dish_id = str(last_dish_id_result.scalar())

        last_dish_data_result = await session.execute(
            select(Dish.title, Dish.description, Dish.price).filter(
                Dish.id == last_dish_id
            )
        )
        title, description, price = last_dish_data_result.one()

    return {
        'id': last_dish_id,
        'title': title,
        'description': description,
        'price': str(price),
    }


@pytest.fixture(scope='session')
async def test_ids():
    return {}


@pytest.fixture
def menu_data():
    return {'title': fake.sentence(), 'description': fake.sentence()}


@pytest.fixture
def dish_data():
    return {
        'title': fake.sentence(),
        'description': fake.sentence(),
        'price': str(
            fake.pydecimal(left_digits=3, right_digits=2, positive=True)
        ),
    }
