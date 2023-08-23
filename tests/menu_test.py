import pytest
from httpx import AsyncClient
from sqlalchemy import select

from src.db.models import Menu
from tests.conftest import async_session_maker


class TestMenu:
    async def test_get_empty_menu_list(self, ac: AsyncClient) -> None:
        response = await ac.get('/api/v1/menus/')
        assert (
            response.status_code == 200
        ), f'Expected status code 200, got {response.status_code} instead'
        response_json = response.json()
        assert response_json == [], f'Expected [] got {response_json} instead'

    @pytest.mark.parametrize(
        'menu_data', [{}], indirect=True, ids=['create_menu']
    )
    async def test_create(
        self,
        ac: AsyncClient,
        menu_data: dict[str, str],
        menu_created_info: dict[str, str],
    ) -> None:
        async with async_session_maker() as session:
            response = await ac.post('/api/v1/menus/', json=menu_data)
            assert (
                response.status_code == 201
            ), f'Expected status code 201, got {response.status_code} instead'

            response_json = response.json()
            menu_id = await session.execute(
                select(Menu.id).order_by(Menu.id.desc()).limit(1)
            )
            last_menu_id = str(menu_id.scalar())
            assert response_json['id'] == last_menu_id, 'Unexpected id'
            assert (
                response_json['title'] == menu_data['title']
            ), 'Unexpected title'
            assert (
                response_json['description'] == menu_data['description']
            ), 'Unexpected description'
            menu_created_info['id'] = last_menu_id
            menu_created_info['description'] = response_json['description']
            menu_created_info['title'] = response_json['title']

    @pytest.mark.parametrize(
        'menu_data', [{}], indirect=True, ids=['patch_menu']
    )
    async def test_patch(
        self,
        ac: AsyncClient,
        menu_data: dict[str, str],
        menu_created_info: dict[str, str],
    ) -> None:
        response = await ac.patch(
            f"/api/v1/menus/{menu_created_info['id']}", json=menu_data
        )
        assert (
            response.status_code == 200
        ), f'Expected status code 200, got {response.status_code} instead'

        response_json = response.json()
        assert response_json['id'] == str(
            menu_created_info['id']
        ), 'Unexpected id'
        assert (
            response_json['title'] != menu_created_info['title']
        ), 'Unexpected title'
        assert (
            response_json['description'] != menu_created_info['description']
        ), 'Unexpected description'
        menu_created_info['description'] = response_json['description']
        menu_created_info['title'] = response_json['title']

    async def test_get_menu(
        self, ac: AsyncClient, menu_created_info: dict[str, str]
    ) -> None:
        response = await ac.get(f"/api/v1/menus/{menu_created_info['id']}")
        assert (
            response.status_code == 200
        ), f'Expected status code 200, got {response.status_code} instead'

        response_json = response.json()

        assert response_json['id'] == str(
            menu_created_info['id']
        ), 'Unexpected id'
        assert (
            response_json['title'] == menu_created_info['title']
        ), 'Unexpected title'
        assert (
            response_json['description'] == menu_created_info['description']
        ), 'Unexpected description'

    async def test_get_menu_list(self, ac: AsyncClient) -> None:
        response = await ac.get('/api/v1/menus/')
        assert (
            response.status_code == 200
        ), f'Expected status code 200, got {response.status_code} instead'

        response_json = response.json()

        assert response_json != [], 'Unexpected empty list []'

    async def test_del_menu(
        self, ac: AsyncClient, menu_created_info: dict[str, str]
    ) -> None:
        response = await ac.delete(f"/api/v1/menus/{menu_created_info['id']}")
        print(response.json())
        assert (
            response.status_code == 200
        ), f'Expected status code 200, got {response.status_code} instead'

    async def test_get_nonexistent_menu(
        self, ac: AsyncClient, menu_created_info: dict[str, str]
    ) -> None:
        response = await ac.get(f"/api/v1/menus/{menu_created_info['id']}")
        assert (
            response.status_code == 404
        ), f'Expected status code 404, got {response.status_code} instead'
        response_json = response.json()
        assert (
            response_json['detail'] == 'menu not found'
        ), 'Expected detail - menu not found'
