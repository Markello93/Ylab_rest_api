import pytest
from httpx import AsyncClient
from sqlalchemy import select

from src.db.models import Dish
from tests.conftest import async_session_maker


class TestDish:
    async def test_get_empty_dishes_list(
        self, ac: AsyncClient, created_submenu: dict[str, str]
    ) -> None:
        response = await ac.get(
            f"/api/v1/menus/{created_submenu['menu_id']}/submenus/{created_submenu['id']}/dishes/"
        )
        assert (
            response.status_code == 200
        ), f'Expected status code 200, got {response.status_code} instead'
        response_json = response.json()
        assert response_json == [], f'Expected [] got {response_json} instead'

    @pytest.mark.parametrize(
        'dish_data', [{}], indirect=True, ids=['create_dish']
    )
    async def test_create(
        self,
        ac: AsyncClient,
        dish_data: dict[str, str],
        created_submenu: dict[str, str],
        dish_created_info: dict[str, str],
    ) -> None:
        async with async_session_maker() as session:
            response = await ac.post(
                f"/api/v1/menus/{created_submenu['menu_id']}/submenus/{created_submenu['id']}/dishes/",
                json=dish_data,
            )
            assert (
                response.status_code == 201
            ), f'Expected status code 201, got {response.status_code} instead'

            response_json = response.json()
            dish_id = await session.execute(
                select(Dish.id).order_by(Dish.id.desc()).limit(1)
            )
            last_dish_id = str(dish_id.scalar())
            assert response_json['id'] == last_dish_id, 'Unexpected id'
            assert (
                response_json['title'] == dish_data['title']
            ), 'Unexpected title'
            assert (
                response_json['description'] == dish_data['description']
            ), 'Unexpected description'
            assert (
                response_json['price'] == dish_data['price']
            ), 'Unexpected price'
            dish_created_info['id'] = response_json['id']
            dish_created_info['title'] = response_json['title']
            dish_created_info['description'] = response_json['description']
            dish_created_info['price'] = response_json['price']
            dish_created_info['submenu_id'] = response_json['submenu_id']
            dish_created_info['menu_id'] = created_submenu['menu_id']

    @pytest.mark.parametrize(
        'dish_data', [{}], indirect=True, ids=['patch_dish']
    )
    async def test_patch(
        self,
        ac: AsyncClient,
        dish_data: dict[str, str],
        dish_created_info: dict[str, str],
    ) -> None:
        response = await ac.patch(
            f"/api/v1/menus/{dish_created_info['menu_id']}/submenus/"
            f"{dish_created_info['submenu_id']}/dishes/{dish_created_info['id']}",
            json=dish_data,
        )
        assert (
            response.status_code == 200
        ), f'Expected status code 200, got {response.status_code} instead'
        response_json = response.json()
        assert response_json['id'] == dish_created_info['id'], 'Unexpected id'
        assert (
            response_json['title'] != dish_created_info['title']
        ), 'Unexpected title'
        assert (
            response_json['description'] != dish_created_info['description']
        ), 'Unexpected description'
        assert (
            response_json['price'] != dish_created_info['price']
        ), 'Unexpected price'
        dish_created_info['title'] = response_json['title']
        dish_created_info['description'] = response_json['description']
        dish_created_info['price'] = response_json['price']

    async def test_get_dish(
        self, ac: AsyncClient, dish_created_info: dict[str, str]
    ) -> None:
        response = await ac.get(
            f"/api/v1/menus/{dish_created_info['menu_id']}/submenus/"
            f"{dish_created_info['submenu_id']}/dishes/{dish_created_info['id']}"
        )
        assert response.status_code == 200
        response_json = response.json()
        assert response_json['id'] == dish_created_info['id'], 'Unexpected id'
        assert (
            response_json['title'] == dish_created_info['title']
        ), 'Unexpected title'
        assert (
            response_json['description'] == dish_created_info['description']
        ), 'Unexpected description'
        assert (
            response_json['price'] == dish_created_info['price']
        ), 'Unexpected price'

    async def test_get_dishes_list(
        self, ac: AsyncClient, dish_created_info: dict[str, str]
    ) -> None:
        response = await ac.get(
            f"/api/v1/menus/{dish_created_info['menu_id']}/submenus/"
            f"{dish_created_info['submenu_id']}/dishes/"
        )
        assert (
            response.status_code == 200
        ), f'Expected status code 200, got {response.status_code} instead'
        response_json = response.json()
        assert response_json != [], 'Got empty list instead of list dishes'

    async def test_del_dish(
        self, ac: AsyncClient, dish_created_info: dict[str, str]
    ) -> None:
        response = await ac.delete(
            f"/api/v1/menus/{dish_created_info['menu_id']}/submenus/"
            f"{dish_created_info['submenu_id']}/dishes/{dish_created_info['id']}"
        )
        assert (
            response.status_code == 200
        ), f'Expected status code 200, got {response.status_code} instead'

    async def test_get_nonexistent_dish(
        self, ac: AsyncClient, dish_created_info: dict[str, str]
    ) -> None:
        response = await ac.get(
            f"/api/v1/menus/{dish_created_info['menu_id']}/submenus/"
            f"{dish_created_info['submenu_id']}/dishes/{dish_created_info['id']}"
        )
        assert (
            response.status_code == 404
        ), f'Expected status code 404, got {response.status_code} instead'
        response_json = response.json()
        assert response_json['detail'] == 'dish not found'
        await ac.delete(f"/api/v1/menus/{dish_created_info['menu_id']}")
