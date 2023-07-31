import pytest
from httpx import AsyncClient
from faker import Faker
from pydantic import UUID4
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.models import Dish

fake = Faker()


@pytest.mark.run(order=11)
async def test_get_empty_dishes_list(ac: AsyncClient, menu_id, submenu_id):
    response = await ac.get(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/")
    assert response.status_code == 200, f"Expected status code 200, got {response.status_code} instead"
    response_json = response.json()
    assert response_json == [], f"Expected [] got {response_json} instead"


@pytest.mark.run(order=12)
async def test_create_dish(ac: AsyncClient, db_session: AsyncSession, menu_id: UUID4, submenu_id: UUID4, last_submenu_data):
    data = {
        "title": fake.sentence(),
        "description": fake.sentence(),
        "price": str(fake.pydecimal(left_digits=3, right_digits=2, positive=True))
    }
    response = await ac.post(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/", json=data)
    assert response.status_code == 201

    response_json = response.json()
    dish_id = await db_session.execute(
        select(Dish.id)
        .order_by(Dish.id.desc())
        .limit(1)
    )
    last_dish_id = str(dish_id.scalar())
    assert response_json["id"] == last_dish_id
    assert response_json["title"] == data["title"]
    assert response_json["description"] == data["description"]
    assert response_json["price"] == data["price"]


@pytest.mark.run(order=13)
async def test_patch_dish(ac: AsyncClient, db_session: AsyncSession, menu_id: UUID4, submenu_id: UUID4, dish_id: UUID4, last_dish_data):
    data = {
    "title": fake.sentence(),
    "description": fake.sentence(),
    "price": str(fake.pydecimal(left_digits=3, right_digits=2, positive=True))
    }
    response = await ac.patch(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}", json=data)
    assert response.status_code == 200
    response_json = response.json()

    assert response_json["title"] != last_dish_data["title"]
    assert response_json["description"] != last_dish_data["description"]
    assert response_json["price"] != last_dish_data["price"]
    assert response_json["id"] == last_dish_data['id']

@pytest.mark.run(order=14)
async def test_get_dish(ac: AsyncClient, db_session: AsyncSession, menu_id: UUID4, submenu_id: UUID4,dish_id: UUID4, last_dish_data,test_ids):

    response = await ac.get(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}")
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["id"] == last_dish_data['id']
    assert response_json["title"] == last_dish_data["title"]
    assert response_json["description"] == last_dish_data["description"]
    test_ids['dish_id'] = last_dish_data['id']


@pytest.mark.run(order=15)
async def test_get_dishes_list(ac: AsyncClient, menu_id, submenu_id):
    response = await ac.get(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/")
    assert response.status_code == 200
    response_json = response.json()
    assert response_json != [], "Got empty list instead of list dishes"


@pytest.mark.run(order=16)
async def test_del_menu(ac: AsyncClient, db_session: AsyncSession, menu_id:UUID4, submenu_id:UUID4,dish_id:str):
    response = await ac.delete(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}")
    assert response.status_code == 200, f"Expected status code 200, got {response.status_code} instead"


@pytest.mark.run(order=17)
async def test_get_nonexistent_dish(ac: AsyncClient, db_session: AsyncSession, test_ids):
    response = await ac.get(f"/api/v1/menus/{test_ids['menu_id']}/submenus/{test_ids['submenu_id']}/dishes/{test_ids['dish_id']}")
    assert response.status_code == 404
    response_json = response.json()
    assert response_json["detail"] == "dish not found"