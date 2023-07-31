import pytest
from httpx import AsyncClient


@pytest.mark.run(order=22)
@pytest.mark.parametrize(
    "menu_data", [{}], indirect=True, ids=["create_scenario_menu"]
)
async def test_menu(ac: AsyncClient, menu_data, test_ids):
    response = await ac.post("/api/v1/menus/", json=menu_data)
    assert (
        response.status_code == 201
    ), f"Expected status code 201, got {response.status_code} instead"

    response_json = response.json()
    assert "id" in response_json, "menu_id not received"
    assert response_json["title"] == menu_data["title"], "Unexpected title"
    assert (
        response_json["description"] == menu_data["description"]
    ), "Unexpected description"
    test_ids["menu_id"] = response_json["id"]


@pytest.mark.run(order=23)
@pytest.mark.parametrize(
    "menu_data", [{}], indirect=True, ids=["create_scenario_submenu"]
)
async def test_submenu(ac: AsyncClient, menu_data, test_ids):
    response = await ac.post(
        f"/api/v1/menus/{test_ids['menu_id']}/submenus/", json=menu_data
    )
    assert (
        response.status_code == 201
    ), f'Expected status code 201, but got "{response.status_code}"'

    response_json = response.json()

    assert "id" in response_json, "submenu_id not received"
    assert response_json["title"] == menu_data["title"], "Unexpected title"
    assert (
        response_json["description"] == menu_data["description"]
    ), "Unexpected description"
    assert (
        response_json["menu_id"] == test_ids["menu_id"]
    ), "Unexpected menu_id"
    test_ids["submenu_id"] = response_json["id"]


@pytest.mark.run(order=24)
@pytest.mark.parametrize(
    "dish_data", [{}], indirect=True, ids=["create_dish_one"]
)
async def test_dish1(ac: AsyncClient, dish_data, test_ids):
    response = await ac.post(
        f"/api/v1/menus/{test_ids['menu_id']}/submenus/{test_ids['submenu_id']}/dishes/",
        json=dish_data,
    )
    assert response.status_code == 201

    response_json = response.json()

    assert "id" in response_json, "dish_id not received"
    assert (
        response_json["title"] == dish_data["title"]
    ), f"expeceted {dish_data['title']}, got {response_json['title']}"
    assert (
        response_json["submenu_id"] == test_ids["submenu_id"]
    ), f"expeceted {test_ids['submenu_id']}, got {response_json['submenu_id']}"
    assert (
        response_json["description"] == dish_data["description"]
    ), f"expeceted {dish_data['description']}, got {response_json['description']}"
    assert response_json["price"] == dish_data["price"]
    test_ids["dish_id_one"] = response_json["id"]


@pytest.mark.run(order=25)
@pytest.mark.parametrize(
    "dish_data", [{}], indirect=True, ids=["create_dish_two"]
)
async def test_dish2(ac: AsyncClient, dish_data, test_ids):
    response = await ac.post(
        f"/api/v1/menus/{test_ids['menu_id']}/submenus/{test_ids['submenu_id']}/dishes/",
        json=dish_data,
    )
    assert (
        response.status_code == 201
    ), f"Expected status code 201, got {response.status_code} instead"
    response_json = response.json()
    assert "id" in response_json, "dish_id not received"
    assert (
        response_json["title"] == dish_data["title"]
    ), f"expeceted {dish_data['title']}, got {response_json['title']}"
    assert (
        response_json["submenu_id"] == test_ids["submenu_id"]
    ), f"expeceted {test_ids['submenu_id']}, got {response_json['submenu_id']}"
    assert (
        response_json["description"] == dish_data["description"]
    ), f"expeceted {dish_data['description']}, got {response_json['description']}"
    assert response_json["price"] == dish_data["price"]
    test_ids["dish_id_two"] = response_json["id"]


@pytest.mark.run(order=26)
async def test_get_scenario_menu(ac: AsyncClient, test_ids):
    response = await ac.get(f"/api/v1/menus/{test_ids['menu_id']}")
    assert (
        response.status_code == 200
    ), f'Expected status code 200, but got "{response.status_code}"'

    response_json = response.json()

    assert response_json != [], f"Expect not empty list"
    assert response_json["id"] == test_ids["menu_id"]
    assert (
        response_json["submenus_count"] == 1
    ), f"Submenus_count = {response_json['submenus_count']}, expected 1"
    assert (
        response_json["dishes_count"] == 2
    ), f"Dishes_count = {response_json['dishes_count']}, expected 2"


@pytest.mark.run(order=27)
async def test_get_scenario_submenu(ac: AsyncClient, test_ids):
    response = await ac.get(
        f"/api/v1/menus/{test_ids['menu_id']}/submenus/{test_ids['submenu_id']}"
    )
    assert (
        response.status_code == 200
    ), f'Expected status code 200, but got "{response.status_code}"'

    response_json = response.json()

    assert (
        response_json["id"] == test_ids["submenu_id"]
    ), f"Expeceted {test_ids['submenu_id']}, got {response_json['submenu_id']}"
    assert (
        response_json["dishes_count"] == 2
    ), f"Dishes_count = {response_json['dishes_count']}, expected 2"


@pytest.mark.run(order=28)
async def test_del_scenario_submenu(ac: AsyncClient, test_ids):
    response = await ac.delete(
        f"/api/v1/menus/{test_ids['menu_id']}/submenus/{test_ids['submenu_id']}"
    )
    assert (
        response.status_code == 200
    ), f'Expected status code 200, but got "{response.status_code}"'


@pytest.mark.run(order=29)
async def test_get_scenario_submenu_list(ac: AsyncClient, test_ids):
    response = await ac.get(f"/api/v1/menus/{test_ids['menu_id']}/submenus/")
    assert (
        response.status_code == 200
    ), f"Expected status code 200, got {response.status_code} instead"
    response_json = response.json()
    assert response_json == []


@pytest.mark.run(order=30)
async def test_get_scenario_empty_dishes_list(ac: AsyncClient, test_ids):
    response = await ac.get(
        f"/api/v1/menus/{test_ids['menu_id']}/submenus/{test_ids['submenu_id']}/dishes/"
    )
    assert (
        response.status_code == 200
    ), f"Expected status code 200, got {response.status_code} instead"
    response_json = response.json()
    assert response_json == [], f"Expected [] got {response_json} instead"


@pytest.mark.run(order=31)
async def test_get_scenario_empty_menu(ac: AsyncClient, test_ids):
    response = await ac.get(f"/api/v1/menus/{test_ids['menu_id']}")
    assert (
        response.status_code == 200
    ), f'Expected status code 200, but got "{response.status_code}"'

    response_json = response.json()

    assert response_json["id"] == test_ids["menu_id"]
    assert (
        response_json["submenus_count"] == 0
    ), f"Submenus_count = {response_json['submenus_count']}, expected 1"
    assert (
        response_json["dishes_count"] == 0
    ), f"Dishes_count = {response_json['dishes_count']}, expected 2"


@pytest.mark.run(order=32)
async def test_del_scenario_menu(ac: AsyncClient, test_ids):
    response = await ac.delete(f"/api/v1/menus/{test_ids['menu_id']}")
    assert (
        response.status_code == 200
    ), f"Expected status code 200, got {response.status_code} instead"


@pytest.mark.run(order=33)
async def test_get_scenario_menu_list(ac: AsyncClient):
    response = await ac.get("/api/v1/menus/")
    assert (
        response.status_code == 200
    ), f"Expected status code 200, got {response.status_code} instead"

    response_json = response.json()

    assert response_json == [], f"Expected [] got {response_json} instead"
