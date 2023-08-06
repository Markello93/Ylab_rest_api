import pytest
from httpx import AsyncClient
from sqlalchemy import select

from src.db.models import Submenu
from tests.conftest import async_session_maker


@pytest.mark.run(order=6)
async def test_get_empty_submenu_list(ac: AsyncClient, test_ids):
    response = await ac.get(f"/api/v1/menus/{test_ids['menu_id']}/submenus/")
    assert (
        response.status_code == 200
    ), f'Expected status code 200, got {response.status_code} instead'
    response_json = response.json()
    assert response_json == [], f'Expected [] got {response_json} instead'


@pytest.mark.run(order=7)
@pytest.mark.parametrize(
    'menu_data', [{}], indirect=True, ids=['create_submenu']
)
async def test_create(
    ac: AsyncClient, menu_data, test_ids
):
    async with async_session_maker() as session:
        response = await ac.post(
            f"/api/v1/menus/{test_ids['menu_id']}/submenus/", json=menu_data
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
        assert response_json['title'] == menu_data['title'], 'Unexpected title'
        assert (
            response_json['description'] == menu_data['description']
        ), 'Unexpected description'
        assert (
            response_json['menu_id'] == test_ids['menu_id']
        ), 'Unexpected menu_id'
        test_ids['submenu_id'] = last_submenu_id


@pytest.mark.run(order=8)
@pytest.mark.parametrize(
    'menu_data', [{}], indirect=True, ids=['patch_submenu']
)
async def test_patch(
    ac: AsyncClient,
    menu_data,
    test_ids,
    last_submenu_data,
):
    response = await ac.patch(
        f"/api/v1/menus/{test_ids['menu_id']}/submenus/{test_ids['submenu_id']}",
        json=menu_data,
    )
    assert (
        response.status_code == 200
    ), f'Expected status code 200, but got "{response.status_code}"'
    response_json = response.json()
    assert response_json['id'] == last_submenu_data['id'], 'Unexpected id'
    assert (
        response_json['title'] != last_submenu_data['title']
    ), 'Unexpected title'
    assert (
        response_json['description'] != last_submenu_data['description']
    ), 'Unexpected description'
    assert (
        response_json['menu_id'] == test_ids['menu_id']
    ), 'Unexpected menu_id'


@pytest.mark.run(order=9)
async def test_get_submenu(
    ac: AsyncClient, test_ids, last_submenu_data
):
    response = await ac.get(
        f"/api/v1/menus/{test_ids['menu_id']}/submenus/{test_ids['submenu_id']}"
    )
    assert (
        response.status_code == 200
    ), f'Expected status code 200, but got "{response.status_code}"'

    response_json = response.json()

    assert response_json['id'] == test_ids['submenu_id'], 'Unexpected id'
    assert (
        response_json['title'] == last_submenu_data['title']
    ), 'Unexpected title'
    assert (
        response_json['description'] == last_submenu_data['description']
    ), 'Unexpected description'


@pytest.mark.run(order=10)
async def test_get_submenu_list(ac: AsyncClient, test_ids):
    response = await ac.get(f"/api/v1/menus/{test_ids['menu_id']}/submenus/")
    assert (
        response.status_code == 200
    ), f'Expected status code 200, but got "{response.status_code}"'
    response_json = response.json()
    assert response_json != [], 'Unexpected empty list []'


@pytest.mark.run(order=18)
async def test_del_submenu(
    ac: AsyncClient, test_ids
):
    response = await ac.delete(
        f"/api/v1/menus/{test_ids['menu_id']}/submenus/{test_ids['submenu_id']}"
    )
    assert (
        response.status_code == 200
    ), f'Expected status code 200, but got "{response.status_code}"'


@pytest.mark.run(order=19)
async def test_get_nonexistent_submenu(
    ac: AsyncClient, test_ids
):
    response = await ac.get(
        f"/api/v1/menus/{test_ids['menu_id']}/submenus/{test_ids['submenu_id']}"
    )
    assert (
        response.status_code == 404
    ), f'Expected status code 404, but got "{response.status_code}"'
    response_json = response.json()
    assert (
        response_json['detail'] == 'submenu not found'
    ), 'Expected detail - submenu not found'
