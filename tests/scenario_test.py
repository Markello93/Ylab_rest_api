import pytest
from httpx import AsyncClient


class TestScenario:
    @pytest.mark.parametrize(
        'menu_data', [{}], indirect=True, ids=['create_scenario_menu']
    )
    async def test_menu(
        self,
        clear_db,
        ac: AsyncClient,
        menu_data,
        menu_created_info: dict[str, str],
    ) -> None:
        response = await ac.post('/api/v1/menus/', json=menu_data)
        assert (
            response.status_code == 201
        ), f'Expected status code 201, got {response.status_code} instead'

        response_json = response.json()
        assert 'id' in response_json, 'menu_id not received'
        assert response_json['title'] == menu_data['title'], 'Unexpected title'
        assert (
            response_json['description'] == menu_data['description']
        ), 'Unexpected description'
        menu_created_info['id'] = response_json['id']
        menu_created_info['title'] = response_json['title']
        menu_created_info['description'] = response_json['description']

    async def test_submenu(
        self,
        ac: AsyncClient,
        menu_data,
        submenu_created_info: dict[str, str],
        menu_created_info: dict[str, str],
    ) -> None:
        response = await ac.post(
            f"/api/v1/menus/{menu_created_info['id']}/submenus/",
            json=menu_data,
        )
        assert (
            response.status_code == 201
        ), f'Expected status code 201, but got "{response.status_code}"'

        response_json = response.json()

        assert 'id' in response_json, 'submenu_id not received'
        assert response_json['title'] == menu_data['title'], 'Unexpected title'
        assert (
            response_json['description'] == menu_data['description']
        ), 'Unexpected description'
        assert (
            response_json['menu_id'] == menu_created_info['id']
        ), 'Unexpected menu_id'
        submenu_created_info['id'] = response_json['id']
        submenu_created_info['title'] = response_json['title']
        submenu_created_info['description'] = response_json['description']
        submenu_created_info['menu_id'] = response_json['menu_id']

    @pytest.mark.parametrize(
        'dish_data', [{}], indirect=True, ids=['create_dish_one']
    )
    async def test_dish1(
        self,
        ac: AsyncClient,
        dish_data,
        submenu_created_info: dict[str, str],
        dish_created_info: dict[str, str],
    ) -> None:
        response = await ac.post(
            f"/api/v1/menus/{submenu_created_info['menu_id']}/submenus/{submenu_created_info['id']}/dishes/",
            json=dish_data,
        )
        assert response.status_code == 201

        response_json = response.json()

        assert 'id' in response_json, 'dish_id not received'
        assert (
            response_json['title'] == dish_data['title']
        ), f"expeceted {dish_data['title']}, got {response_json['title']}"
        assert (
            response_json['submenu_id'] == submenu_created_info['id']
        ), f"expeceted {submenu_created_info['id']}, got {response_json['submenu_id']}"
        assert (
            response_json['description'] == dish_data['description']
        ), f"expeceted {dish_data['description']}, got {response_json['description']}"
        assert response_json['price'] == dish_data['price']
        dish_created_info['dish_id_one'] = response_json['id']

    @pytest.mark.parametrize(
        'dish_data', [{}], indirect=True, ids=['create_dish_two']
    )
    async def test_dish2(
        self,
        ac: AsyncClient,
        dish_data,
        submenu_created_info: dict[str, str],
        dish_created_info: dict[str, str],
    ) -> None:
        response = await ac.post(
            f"/api/v1/menus/{submenu_created_info['menu_id']}/submenus/{submenu_created_info['id']}/dishes/",
            json=dish_data,
        )
        assert (
            response.status_code == 201
        ), f'Expected status code 201, got {response.status_code} instead'
        response_json = response.json()
        assert 'id' in response_json, 'dish_id not received'
        assert (
            response_json['title'] == dish_data['title']
        ), f"expeceted {dish_data['title']}, got {response_json['title']}"
        assert (
            response_json['submenu_id'] == submenu_created_info['id']
        ), f"expeceted {submenu_created_info['id']}, got {response_json['submenu_id']}"
        assert (
            response_json['description'] == dish_data['description']
        ), f"expeceted {dish_data['description']}, got {response_json['description']}"
        assert response_json['price'] == dish_data['price']
        dish_created_info['dish_id_two'] = response_json['id']

    async def test_get_scenario_menu(
        self, ac: AsyncClient, menu_created_info: dict[str, str]
    ) -> None:
        response = await ac.get(f"/api/v1/menus/{menu_created_info['id']}")
        assert (
            response.status_code == 200
        ), f'Expected status code 200, but got "{response.status_code}"'

        response_json = response.json()

        assert response_json != [], 'Expect not empty list'
        assert response_json['id'] == menu_created_info['id']
        assert (
            response_json['submenus_count'] == 1
        ), f"Submenus_count = {response_json['submenus_count']}, expected 1"
        assert (
            response_json['dishes_count'] == 2
        ), f"Dishes_count = {response_json['dishes_count']}, expected 2"

    async def test_get_scenario_submenu(
        self, ac: AsyncClient, submenu_created_info: dict[str, str]
    ) -> None:
        response = await ac.get(
            f"/api/v1/menus/{submenu_created_info['menu_id']}/submenus/{submenu_created_info['id']}"
        )
        assert (
            response.status_code == 200
        ), f'Expected status code 200, but got "{response.status_code}"'

        response_json = response.json()

        assert (
            response_json['id'] == submenu_created_info['id']
        ), f"Expeceted {submenu_created_info['id']}, got {response_json['id']}"
        assert (
            response_json['dishes_count'] == 2
        ), f"Dishes_count = {response_json['dishes_count']}, expected 2"

    async def test_del_scenario_submenu(
        self, ac: AsyncClient, submenu_created_info: dict[str, str]
    ) -> None:
        response = await ac.delete(
            f"/api/v1/menus/{submenu_created_info['menu_id']}/submenus/{submenu_created_info['id']}"
        )
        assert (
            response.status_code == 200
        ), f'Expected status code 200, but got "{response.status_code}"'

    async def test_get_scenario_submenu_list(
        self, ac: AsyncClient, submenu_created_info: dict[str, str]
    ) -> None:
        response = await ac.get(
            f"/api/v1/menus/{submenu_created_info['menu_id']}/submenus/"
        )
        assert (
            response.status_code == 200
        ), f'Expected status code 200, got {response.status_code} instead'
        response_json = response.json()
        assert response_json == []

    async def test_get_scenario_empty_dishes_list(
        self, ac: AsyncClient, submenu_created_info: dict[str, str]
    ) -> None:
        response = await ac.get(
            f"/api/v1/menus/{submenu_created_info['menu_id']}/submenus/{submenu_created_info['id']}/dishes/"
        )
        assert (
            response.status_code == 200
        ), f'Expected status code 200, got {response.status_code} instead'
        response_json = response.json()
        assert response_json == [], f'Expected [] got {response_json} instead'

    async def test_get_scenario_empty_menu(
        self, ac: AsyncClient, submenu_created_info: dict[str, str]
    ) -> None:
        response = await ac.get(
            f"/api/v1/menus/{submenu_created_info['menu_id']}"
        )
        assert (
            response.status_code == 200
        ), f'Expected status code 200, but got "{response.status_code}"'

        response_json = response.json()

        assert response_json['id'] == submenu_created_info['menu_id']
        assert (
            response_json['submenus_count'] == 0
        ), f"Submenus_count = {response_json['submenus_count']}, expected 1"
        assert (
            response_json['dishes_count'] == 0
        ), f"Dishes_count = {response_json['dishes_count']}, expected 2"

    async def test_del_scenario_menu(
        self, ac: AsyncClient, submenu_created_info: dict[str, str]
    ) -> None:
        response = await ac.delete(
            f"/api/v1/menus/{submenu_created_info['menu_id']}"
        )
        assert (
            response.status_code == 200
        ), f'Expected status code 200, got {response.status_code} instead'

    async def test_get_scenario_menu_list(
        self, ac: AsyncClient, submenu_created_info
    ) -> None:
        response = await ac.get('/api/v1/menus/')
        assert (
            response.status_code == 200
        ), f'Expected status code 200, got {response.status_code} instead'

        response_json = response.json()

        assert response_json == [], f'Expected [] got {response_json} instead'
        await ac.delete(f"/api/v1/menus/{submenu_created_info['menu_id']}")
