import pytest
from httpx import AsyncClient
from faker import Faker
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.models import Menu

fake = Faker()


@pytest.mark.run(order=1)
async def test_get_empty_menu_list(ac: AsyncClient):
    response = await ac.get("/api/v1/menus/")
    assert (
        response.status_code == 200
    ), f"Expected status code 200, got {response.status_code} instead"
    response_json = response.json()
    assert response_json == [], f"Expected [] got {response_json} instead"


@pytest.mark.run(order=2)
@pytest.mark.parametrize("menu_data", [{}], indirect=True, ids=["create_menu"])
async def test_create(
    ac: AsyncClient, db_session: AsyncSession, menu_data, test_ids
):
    response = await ac.post("/api/v1/menus/", json=menu_data)
    assert (
        response.status_code == 201
    ), f"Expected status code 201, got {response.status_code} instead"

    response_json = response.json()
    menu_id = await db_session.execute(
        select(Menu.id).order_by(Menu.id.desc()).limit(1)
    )
    last_menu_id = str(menu_id.scalar())
    assert response_json["id"] == last_menu_id, "Unexpected id"
    assert response_json["title"] == menu_data["title"], "Unexpected title"
    assert (
        response_json["description"] == menu_data["description"]
    ), "Unexpected description"
    test_ids["menu_id"] = last_menu_id


@pytest.mark.run(order=3)
@pytest.mark.parametrize("menu_data", [{}], indirect=True, ids=["patch_menu"])
async def test_patch(ac: AsyncClient, test_ids, menu_data, last_menu_data):
    response = await ac.patch(
        f"/api/v1/menus/{test_ids['menu_id']}", json=menu_data
    )
    assert (
        response.status_code == 200
    ), f"Expected status code 200, got {response.status_code} instead"

    response_json = response.json()
    assert response_json["id"] == str(test_ids["menu_id"]), "Unexpected id"
    assert (
        response_json["title"] != last_menu_data["title"]
    ), "Unexpected title"
    assert (
        response_json["description"] != last_menu_data["description"]
    ), "Unexpected description"


@pytest.mark.run(order=4)
async def test_get_menu(ac: AsyncClient, test_ids, last_menu_data):
    response = await ac.get(f"/api/v1/menus/{test_ids['menu_id']}")
    assert (
        response.status_code == 200
    ), f"Expected status code 200, got {response.status_code} instead"

    response_json = response.json()

    assert response_json["id"] == str(test_ids["menu_id"]), "Unexpected id"
    assert (
        response_json["title"] == last_menu_data["title"]
    ), "Unexpected title"
    assert (
        response_json["description"] == last_menu_data["description"]
    ), "Unexpected description"


@pytest.mark.run(order=5)
async def test_get_menu_list(ac: AsyncClient):
    response = await ac.get("/api/v1/menus/")
    assert (
        response.status_code == 200
    ), f"Expected status code 200, got {response.status_code} instead"

    response_json = response.json()

    assert response_json != [], f"Unexpected empty list []"


@pytest.mark.run(order=20)
async def test_del_menu(ac: AsyncClient, db_session: AsyncSession, test_ids):
    response = await ac.delete(f"/api/v1/menus/{test_ids['menu_id']}")
    assert (
        response.status_code == 200
    ), f"Expected status code 200, got {response.status_code} instead"


@pytest.mark.run(order=21)
async def test_get_nonexistent_menu(ac: AsyncClient, test_ids):
    response = await ac.get(f"/api/v1/menus/{test_ids['menu_id']}")
    assert (
        response.status_code == 404
    ), f"Expected status code 404, got {response.status_code} instead"
    response_json = response.json()
    assert (
        response_json["detail"] == "menu not found"
    ), "Expected detail - menu not found"
