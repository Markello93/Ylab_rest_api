import pytest
from httpx import AsyncClient
from faker import Faker
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.models import Dish

fake = Faker()


@pytest.mark.run(order=11)
async def test_get_empty_dishes_list(ac: AsyncClient, test_ids):
    response = await ac.get(
        f"/api/v1/menus/{test_ids['menu_id']}/submenus/{test_ids['submenu_id']}/dishes/"
    )
    assert (
        response.status_code == 200
    ), f"Expected status code 200, got {response.status_code} instead"
    response_json = response.json()
    assert response_json == [], f"Expected [] got {response_json} instead"


@pytest.mark.run(order=12)
@pytest.mark.parametrize("dish_data", [{}], indirect=True, ids=["create_dish"])
async def test_create(
    ac: AsyncClient,
    db_session: AsyncSession,
    dish_data,
    test_ids,
    last_submenu_data,
):
    response = await ac.post(
        f"/api/v1/menus/{test_ids['menu_id']}/submenus/{test_ids['submenu_id']}/dishes/",
        json=dish_data,
    )
    assert (
        response.status_code == 201
    ), f"Expected status code 201, got {response.status_code} instead"

    response_json = response.json()
    dish_id = await db_session.execute(
        select(Dish.id).order_by(Dish.id.desc()).limit(1)
    )
    last_dish_id = str(dish_id.scalar())
    assert response_json["id"] == last_dish_id, "Unexpected id"
    assert response_json["title"] == dish_data["title"], "Unexpected title"
    assert (
        response_json["description"] == dish_data["description"]
    ), "Unexpected description"
    assert response_json["price"] == dish_data["price"], "Unexpected price"
    test_ids["dish_id"] = last_dish_id


@pytest.mark.run(order=13)
@pytest.mark.parametrize("dish_data", [{}], indirect=True, ids=["patch_dish"])
async def test_patch(
    ac: AsyncClient,
    db_session: AsyncSession,
    dish_data,
    test_ids,
    last_dish_data,
):
    response = await ac.patch(
        f"/api/v1/menus/{test_ids['menu_id']}/submenus/"
        f"{test_ids['submenu_id']}/dishes/{test_ids['dish_id']}",
        json=dish_data,
    )
    assert (
        response.status_code == 200
    ), f"Expected status code 200, got {response.status_code} instead"
    response_json = response.json()
    assert response_json["id"] == last_dish_data["id"], "Unexpected id"
    assert (
        response_json["title"] != last_dish_data["title"]
    ), "Unexpected title"
    assert (
        response_json["description"] != last_dish_data["description"]
    ), "Unexpected description"
    assert (
        response_json["price"] != last_dish_data["price"]
    ), "Unexpected price"


@pytest.mark.run(order=14)
async def test_get_dish(ac: AsyncClient, last_dish_data, test_ids):
    response = await ac.get(
        f"/api/v1/menus/{test_ids['menu_id']}/submenus/"
        f"{test_ids['submenu_id']}/dishes/{test_ids['dish_id']}"
    )
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["id"] == last_dish_data["id"], "Unexpected id"
    assert (
        response_json["title"] == last_dish_data["title"]
    ), "Unexpected title"
    assert (
        response_json["description"] == last_dish_data["description"]
    ), "Unexpected description"


@pytest.mark.run(order=15)
async def test_get_dishes_list(ac: AsyncClient, test_ids):
    response = await ac.get(
        f"/api/v1/menus/{test_ids['menu_id']}/submenus/"
        f"{test_ids['submenu_id']}/dishes/"
    )
    assert (
        response.status_code == 200
    ), f"Expected status code 200, got {response.status_code} instead"
    response_json = response.json()
    assert response_json != [], "Got empty list instead of list dishes"


@pytest.mark.run(order=16)
async def test_del_dish(ac: AsyncClient, test_ids):
    response = await ac.delete(
        f"/api/v1/menus/{test_ids['menu_id']}/submenus/"
        f"{test_ids['submenu_id']}/dishes/{test_ids['dish_id']}"
    )
    assert (
        response.status_code == 200
    ), f"Expected status code 200, got {response.status_code} instead"


@pytest.mark.run(order=17)
async def test_get_nonexistent_dish(
    ac: AsyncClient, db_session: AsyncSession, test_ids
):
    response = await ac.get(
        f"/api/v1/menus/{test_ids['menu_id']}/submenus/"
        f"{test_ids['submenu_id']}/dishes/{test_ids['dish_id']}"
    )
    assert (
        response.status_code == 404
    ), f"Expected status code 404, got {response.status_code} instead"
    response_json = response.json()
    assert response_json["detail"] == "dish not found"
