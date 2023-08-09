from http import HTTPStatus
from typing import Optional

from fastapi import APIRouter, Depends, Path
from fastapi.responses import JSONResponse
from fastapi_restful.cbv import cbv
from pydantic import UUID4

from src.api.request_models.request_base import DishRequest
from src.api.response_models.dish_response import DishResponse
from src.services.dishes_service import DishService

dishes_router = APIRouter(
    prefix='/menus/{menu_id}/submenus/{submenu_id}/dishes', tags=['Dishes']
)


@cbv(dishes_router)
class DishCBV:
    """Class that combines requests for a Dish model."""

    __dish_service: DishService = Depends()

    @dishes_router.post(
        '/',
        summary='Create a new dish',
        description='To create a menu, send a POST request with JSON data containing the "title", "description" '
        'and "price" fields in string format, price must be writen as number(decimal or int).',
        response_model=DishResponse,
        status_code=HTTPStatus.CREATED,
        response_description='The created dish',
    )
    async def create_dish_router(
        self, menu_id: UUID4, submenu_id: UUID4, schema: DishRequest
    ) -> DishResponse:
        return await self.__dish_service.create_dish(
            menu_id, submenu_id, schema
        )

    @dishes_router.get(
        '/{dish_id}',
        summary='Get a dish by ID',
        description='To retrieve a dish, send a GET request with the "menu_id" ,'
        ' "submenu_id" and "dish_id" parameters in the URL.',
        response_model=DishResponse,
        response_description='The requested dish',
    )
    async def get_dish_router(
        self, menu_id: UUID4, submenu_id: UUID4, dish_id: UUID4
    ) -> DishResponse:
        return await self.__dish_service.get_dish(menu_id, submenu_id, dish_id)

    @dishes_router.patch(
        '/{dish_id}',
        summary='Update a dish by ID',
        description='To update a dish, send a PATCH request with the dish_id parameter in the URL '
        'and JSON data containing the "title",'
        ' "description" and "price" fields in string format in the request body,'
        ' price must be writen as number(decimal or int).',
        response_model=Optional[DishResponse],
        status_code=HTTPStatus.OK,
        response_description='The dish with changes',
    )
    async def update_dish_router(
        self,
        schema: DishRequest,
        menu_id: UUID4 = Path(
            ..., description='The ID of the menu related to this dish'
        ),
        submenu_id: UUID4 = Path(
            ..., description='The ID of the menu to update'
        ),
        dish_id: UUID4 = Path(..., description='The ID of the menu to update'),
    ) -> DishResponse:
        return await self.__dish_service.update_dish(
            menu_id, submenu_id, dish_id, schema
        )

    @dishes_router.delete(
        '/{dish_id}',
        summary='Delete a dish by ID',
        description='To delete a dish, send a DELETE request with the dish parameter in the URL.',
        response_model=None,
        status_code=HTTPStatus.OK,
        response_description='Returns an empty JSON with status code 200 if deletion was successful',
    )
    async def delete_dish_router(
        self,
        menu_id: UUID4 = Path(
            ..., description='The ID of the menu related to this dish'
        ),
        submenu_id: UUID4 = Path(
            ..., description='The ID of the submenu related to this dish'
        ),
        dish_id: UUID4 = Path(..., description='The ID of the dish to delete'),
    ) -> JSONResponse:
        await self.__dish_service.delete_dish(menu_id, submenu_id, dish_id)
        return JSONResponse(content={}, status_code=HTTPStatus.OK)

    @dishes_router.get(
        '/',
        summary='Get a list of available dishes',
        description='To retrieve dishes, send a GET request to the "dishes" URL path.',
        response_model=list[DishResponse],
        status_code=HTTPStatus.OK,
        response_description='Returns a list of dishes,'
        ' or an empty list if no dishes have been created',
    )
    async def get_dishes_router(
        self, menu_id: UUID4, submenu_id: UUID4
    ) -> list[DishResponse]:
        return await self.__dish_service.get_dishes(menu_id, submenu_id)
