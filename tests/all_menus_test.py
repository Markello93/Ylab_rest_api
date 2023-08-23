from httpx import AsyncClient


class TestDataGenerator:
    async def generate_test_data(
        self,
        ac: AsyncClient,
        menu_data: dict,
        submenu_data: dict,
        dish_data: dict,
    ) -> tuple:
        response_menu = await ac.post('/api/v1/menus/', json=menu_data)
        expected_menu = response_menu.json()
        response_submenu = await ac.post(
            f"/api/v1/menus/{expected_menu['id']}/submenus/", json=submenu_data
        )
        expected_submenu = response_submenu.json()
        response_dish = await ac.post(
            f"/api/v1/menus/{expected_menu['id']}/submenus/{expected_submenu['id']}/dishes/",
            json=dish_data,
        )
        expected_dish = response_dish.json()

        return expected_menu, expected_submenu, expected_dish


async def test_check_all_menus(ac: AsyncClient, clear_db) -> None:
    menu_data = {
        'title': 'Default Menu',
        'description': 'Default Menu Description',
    }
    submenu_data = {
        'title': 'Default Submenu',
        'description': 'Default Submenu Description',
    }
    dish_data = {
        'title': 'Default Dish',
        'description': 'Default Dish Description',
        'price': 10.0,
    }

    data_generator = TestDataGenerator()
    (
        expected_menu,
        expected_submenu,
        expected_dish,
    ) = await data_generator.generate_test_data(
        ac, menu_data, submenu_data, dish_data
    )

    response = await ac.get('/api/v1/menus/menus_info/')
    assert response.status_code == 200

    received_data = response.json()
    assert len(received_data) == 1

    received_menu = received_data[0]
    assert received_menu['id'] == expected_menu['id']
    assert received_menu['title'] == expected_menu['title']
    assert received_menu['description'] == expected_menu['description']

    received_submenus = received_menu['submenus']
    assert len(received_submenus) == 1

    received_submenu = received_submenus[0]
    assert received_submenu['id'] == expected_submenu['id']
    assert received_submenu['title'] == expected_submenu['title']
    assert received_submenu['description'] == expected_submenu['description']

    received_dishes = received_submenu['dishes']
    assert len(received_dishes) == 1

    received_dish = received_dishes[0]
    assert received_dish['id'] == expected_dish['id']
    assert received_dish['title'] == expected_dish['title']
    assert received_dish['description'] == expected_dish['description']
    assert str(received_dish['price']) == expected_dish['price']

    await ac.delete(f"/api/v1/menus/{received_menu['id']}")
