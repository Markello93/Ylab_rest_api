import pytest
from httpx import AsyncClient
from faker import Faker
from pydantic import UUID4
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.models import Menu

fake = Faker()


@pytest.mark.run(order=1)
async def test_get_empty_menu_list(ac: AsyncClient):
    response = await ac.get("/api/v1/menus/")
    assert response.status_code == 200
    response_json = response.json()
    assert response_json == []


@pytest.mark.run(order=2)
async def test_create_menu(ac: AsyncClient, db_session: AsyncSession, test_ids):
    data = {
    "title": fake.sentence(),
    "description": fake.sentence()
    }
    response = await ac.post("/api/v1/menus/", json=data)
    assert response.status_code == 201

    response_json = response.json()
    menu_id = await db_session.execute(
        select(Menu.id)
        .order_by(Menu.id.desc())
        .limit(1)
    )
    last_menu_id = str(menu_id.scalar())
    assert response_json["id"] == last_menu_id
    assert response_json["title"] == data["title"]
    assert response_json["description"] == data["description"]
    test_ids['menu_id'] = last_menu_id


@pytest.mark.run(order=3)
async def test_patch_menu(ac: AsyncClient, test_ids, last_menu_data):
    data = {
    "title": fake.sentence(),
    "description": fake.sentence()
    }
    response = await ac.patch(f"/api/v1/menus/{test_ids['menu_id']}", json=data)
    assert response.status_code == 200

    response_json = response.json()
    assert response_json["id"] == str(test_ids['menu_id'])
    assert response_json["title"] != last_menu_data["title"]
    assert response_json["description"] != last_menu_data["description"]


@pytest.mark.run(order=4)
async def test_get_menu(ac: AsyncClient, test_ids, last_menu_data):
    response = await ac.get(f"/api/v1/menus/{test_ids['menu_id']}")
    assert response.status_code == 200

    response_json = response.json()

    assert response_json["id"] == str(test_ids['menu_id'])
    assert response_json["title"] == last_menu_data["title"]
    assert response_json["description"] == last_menu_data["description"]


@pytest.mark.run(order=5)
async def test_get_menu_list(ac: AsyncClient):
    response = await ac.get("/api/v1/menus/")
    assert response.status_code == 200

    response_json = response.json()

    assert response_json != []


@pytest.mark.run(order=20)
async def test_del_menu(ac: AsyncClient, db_session: AsyncSession, test_ids):

    response = await ac.delete(f"/api/v1/menus/{test_ids['menu_id']}")
    assert response.status_code == 200


@pytest.mark.run(order=21)
async def test_get_nonexistent_menu(ac: AsyncClient, test_ids):
    response = await ac.get(f"/api/v1/menus/{test_ids['menu_id']}")
    print(response.json())
    assert response.status_code == 404
    response_json = response.json()
    assert response_json["detail"] == "menu not found"




