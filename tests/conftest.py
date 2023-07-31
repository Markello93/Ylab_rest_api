import asyncio
from typing import AsyncGenerator

import pytest
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from run import app
from src.core.settings import get_settings
from src.db.db import get_session
from src.db.models import Dish, Menu, Submenu


@pytest.fixture(scope='session')
def event_loop():
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def app_settings():
    return get_settings()


@pytest.fixture(scope="session")
async def ac(app_settings, event_loop) -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(
            app=app,
            base_url=f"http://{app_settings.DB_HOST}:{app_settings.DB_PORT}"
    ) as ac:
        yield ac


@pytest.fixture(scope="session")
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    async for session in get_session():
        yield session




# @pytest.fixture(scope="session")
# async def last_menu_id(db_session):
#     # last_menu_id_result = await db_session.execute(select(Menu.id).order_by(Menu.id.desc()).limit(1))
#     last_menu_id_result = await db_session.execute(
#             select(Menu.id)
#             .order_by(Menu.id.desc())
#             .limit(1)
#         )
#     last_menu_id = str(last_menu_id_result.scalar())
#     return last_menu_id


@pytest.fixture(scope='function')
async def last_menu_data(db_session):
    last_menu_id_result = await db_session.execute(
        select(Menu.id)
        .order_by(Menu.id.desc())
        .limit(1)
    )
    last_menu_id = str(last_menu_id_result.scalar())

    # Получаем description и title по last_menu_id
    last_menu_data_result = await db_session.execute(
        select(Menu.description, Menu.title)
        .filter(Menu.id == last_menu_id)
    )
    description, title = last_menu_data_result.one()

    return {
        "id": last_menu_id,
        "description": description,
        "title": title
    }

# @pytest.fixture(scope="session")
# async def last_submenu_id(db_session):
#     # last_menu_id_result = await db_session.execute(select(Menu.id).order_by(Menu.id.desc()).limit(1))
#     last_submenu_id_result = await db_session.execute(
#             select(Submenu.id)
#             .order_by(Submenu.id.desc())
#             .limit(1)
#         )
#     last_submenu_id = str(last_submenu_id_result.scalar())
#     return last_submenu_id


@pytest.fixture(scope='function')
async def last_submenu_data(db_session):
    last_submenu_id_result = await db_session.execute(
            select(Submenu.id)
            .order_by(Submenu.id.desc())
            .limit(1)
        )
    last_submenu_id = str(last_submenu_id_result.scalar())

    # Получаем description и title по last_menu_id
    last_submenu_data_result = await db_session.execute(
        select(Submenu.description, Submenu.title)
        .filter(Submenu.id == last_submenu_id)
    )
    description, title = last_submenu_data_result.one()

    return {
        "id": last_submenu_id,
        "description": description,
        "title": title
    }

# @pytest.fixture(scope="function")
# async def last_dish_id(db_session):
#     last_dish_id_result = await db_session.execute(
#             select(Dish.id)
#             .order_by(Dish.id.desc())
#             .limit(1)
#         )
#     last_dish_id = str(last_dish_id_result.scalar())
#     return last_dish_id


@pytest.fixture(scope='function')
async def last_dish_data(db_session):
    last_dish_id_result = await db_session.execute(
            select(Dish.id)
            .order_by(Dish.id.desc())
            .limit(1)
        )
    last_dish_id = str(last_dish_id_result.scalar())

    # Получаем description и title по last_menu_id
    last_dish_data_result = await db_session.execute(
        select(Dish.title, Dish.description, Dish.price)
        .filter(Dish.id == last_dish_id)
    )
    title, description, price = last_dish_data_result.one()

    return {
        "id": last_dish_id,
        "title": title,
        "description": description,
        "price": str(price)
    }


@pytest.fixture(scope="function")
async def menu_id(db_session):
    async with db_session as session:
        return await session.scalar(select(Menu.id))

@pytest.fixture(scope="function")
async def submenu_id(db_session):
    async with db_session as session:
        return await session.scalar(select(Submenu.id))

@pytest.fixture(scope="function")
async def dish_id(db_session):
    async with db_session as session:
        return await session.scalar(select(Dish.id))

@pytest.fixture(scope='session')
async def test_ids():
    return {}