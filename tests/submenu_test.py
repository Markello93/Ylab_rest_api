import pytest
from httpx import AsyncClient
from faker import Faker
from pydantic import UUID4
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.models import Submenu

fake = Faker()


@pytest.mark.run(order=6)
async def test_get_empty_submenu_list(ac: AsyncClient, test_ids):
    response = await ac.get(f"/api/v1/menus/{test_ids['menu_id']}/submenus/")
    assert response.status_code == 200
    response_json = response.json()
    assert response_json == []


@pytest.mark.run(order=7)
async def test_create_submenu(ac: AsyncClient, db_session: AsyncSession, test_ids, last_menu_data):
    data = {
        "title": fake.sentence(),
        "description": fake.sentence()
    }
    response = await ac.post(f"/api/v1/menus/{test_ids['menu_id']}/submenus/", json=data)
    assert response.status_code == 201, f'Expected status code 201, but got "{response.status_code}"'

    response_json = response.json()
    submenu_id = await db_session.execute(
        select(Submenu.id)
        .order_by(Submenu.id.desc())
        .limit(1)
    )
    last_submenu_id = str(submenu_id.scalar())

    assert response_json["id"] == last_submenu_id
    assert response_json["title"] == data["title"]
    assert response_json["description"] == data["description"]
    assert response_json["menu_id"] == test_ids['menu_id']
    test_ids['submenu_id'] = last_submenu_id


@pytest.mark.run(order=8)
async def test_patch_submenu(ac: AsyncClient, db_session: AsyncSession, test_ids,last_submenu_data):
    data = {
    "title": fake.sentence(),
    "description": fake.sentence()
    }
    response = await ac.patch(f"/api/v1/menus/{test_ids['menu_id']}/submenus/{test_ids['submenu_id']}",json=data)
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["title"] != last_submenu_data["title"]
    assert response_json["description"] != last_submenu_data["description"]
    assert response_json["id"] == last_submenu_data['id']
    assert response_json["menu_id"] == test_ids['menu_id']


@pytest.mark.run(order=9)
async def test_get_submenu(ac: AsyncClient, db_session: AsyncSession, test_ids, last_submenu_data):
    response = await ac.get(f"/api/v1/menus/{test_ids['menu_id']}/submenus/{test_ids['submenu_id']}")
    assert response.status_code == 200

    response_json = response.json()

    assert response_json["id"] == test_ids['submenu_id']
    assert response_json["title"] == last_submenu_data["title"]
    assert response_json["description"] == last_submenu_data["description"]


@pytest.mark.run(order=10)
async def test_get_submenu_list(ac: AsyncClient, test_ids):
    response = await ac.get(f"/api/v1/menus/{test_ids['menu_id']}/submenus/")
    assert response.status_code == 200
    response_json = response.json()
    assert response_json != []


@pytest.mark.run(order=18)
async def test_del_submenu(ac: AsyncClient, db_session: AsyncSession, test_ids):

    response = await ac.delete(f"/api/v1/menus/{test_ids['menu_id']}/submenus/{test_ids['submenu_id']}")
    assert response.status_code == 200


@pytest.mark.run(order=19)
async def test_get_nonexistent_submenu(ac: AsyncClient, db_session: AsyncSession, test_ids):
    response = await ac.get(f"/api/v1/menus/{test_ids['menu_id']}/submenus/{test_ids['submenu_id']}")
    assert response.status_code == 404
    response_json = response.json()
    assert response_json["detail"] == "submenu not found"