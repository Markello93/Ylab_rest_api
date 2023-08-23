import pytest
from httpx import AsyncClient
from sqlalchemy import select

from src.db.models import Submenu
from tests.conftest import async_session_maker


class TestSubmenu:
    async def test_get_empty_submenu_list(
        self, ac: AsyncClient, created_menu: dict[str, str]
    ) -> None:
        response = await ac.get(
            f"/api/v1/menus/{created_menu['id']}/submenus/"
        )
        assert (
            response.status_code == 200
        ), f'Expected status code 200, got {response.status_code} instead'
        response_json = response.json()
        assert response_json == [], f'Expected [] got {response_json} instead'

    @pytest.mark.parametrize(
        'menu_data', [{}], indirect=True, ids=['create_submenu']
    )
    async def test_create(
        self,
        ac: AsyncClient,
        menu_data: dict[str, str],
        created_menu: dict[str, str],
        submenu_created_info: dict[str, str],
    ) -> None:
        async with async_session_maker() as session:
            response = await ac.post(
                f"/api/v1/menus/{created_menu['id']}/submenus/", json=menu_data
            )
            assert (
                response.status_code == 201
            ), f'Expected status code 201, but got "{response.status_code}"'

            response_json = response.json()
            submenu_id = await session.execute(
                select(Submenu.id).order_by(Submenu.id.desc()).limit(1)
            )
            last_submenu_id = str(submenu_id.scalar())

            assert response_json['id'] == last_submenu_id, 'Unexpected id'
            assert (
                response_json['title'] == menu_data['title']
            ), 'Unexpected title'
            assert (
                response_json['description'] == menu_data['description']
            ), 'Unexpected description'
            assert (
                response_json['menu_id'] == created_menu['id']
            ), 'Unexpected menu_id'
            submenu_created_info['id'] = last_submenu_id
            submenu_created_info['title'] = response_json['title']
            submenu_created_info['description'] = response_json['description']
            submenu_created_info['menu_id'] = response_json['menu_id']

    @pytest.mark.parametrize(
        'menu_data', [{}], indirect=True, ids=['patch_submenu']
    )
    async def test_patch(
        self,
        ac: AsyncClient,
        menu_data: dict[str, str],
        submenu_created_info: dict[str, str],
    ) -> None:
        response = await ac.patch(
            f"/api/v1/menus/{submenu_created_info['menu_id']}/submenus/{submenu_created_info['id']}",
            json=menu_data,
        )
        assert (
            response.status_code == 200
        ), f'Expected status code 200, but got "{response.status_code}"'
        response_json = response.json()
        print(response_json)
        assert (
            response_json['id'] == submenu_created_info['id']
        ), 'Unexpected id'
        assert (
            response_json['title'] != submenu_created_info['title']
        ), 'Unexpected title'
        assert (
            response_json['description'] != submenu_created_info['description']
        ), 'Unexpected description'
        assert (
            response_json['menu_id'] == submenu_created_info['menu_id']
        ), 'Unexpected menu_id'
        submenu_created_info['description'] = response_json['description']
        submenu_created_info['title'] = response_json['title']

    async def test_get_submenu(
        self,
        ac: AsyncClient,
        submenu_created_info: dict[str, str],
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
        ), 'Unexpected id'
        assert (
            response_json['title'] == submenu_created_info['title']
        ), 'Unexpected title'
        assert (
            response_json['description'] == submenu_created_info['description']
        ), 'Unexpected description'

    async def test_get_submenu_list(
        self, ac: AsyncClient, submenu_created_info: dict[str, str]
    ) -> None:
        response = await ac.get(
            f"/api/v1/menus/{submenu_created_info['menu_id']}/submenus/"
        )
        assert (
            response.status_code == 200
        ), f'Expected status code 200, but got "{response.status_code}"'
        response_json = response.json()
        assert response_json != [], 'Unexpected empty list []'

    async def test_del_submenu(
        self, ac: AsyncClient, submenu_created_info: dict[str, str]
    ) -> None:
        response = await ac.delete(
            f"/api/v1/menus/{submenu_created_info['menu_id']}/submenus/{submenu_created_info['id']}"
        )
        assert (
            response.status_code == 200
        ), f'Expected status code 200, but got "{response.status_code}"'

    async def test_get_nonexistent_submenu(
        self, ac: AsyncClient, submenu_created_info: dict[str, str]
    ) -> None:
        response = await ac.get(
            f"/api/v1/menus/{submenu_created_info['menu_id']}/submenus/{submenu_created_info['id']}"
        )
        assert (
            response.status_code == 404
        ), f'Expected status code 404, but got "{response.status_code}"'
        response_json = response.json()
        assert (
            response_json['detail'] == 'submenu not found'
        ), 'Expected detail - submenu not found'
        await ac.delete(f"/api/v1/menus/{submenu_created_info['menu_id']}")
