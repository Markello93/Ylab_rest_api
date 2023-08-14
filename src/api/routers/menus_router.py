from http import HTTPStatus

from fastapi import APIRouter, Depends, Path
from fastapi.responses import JSONResponse
from fastapi_restful.cbv import cbv
from pydantic import UUID4

from src.api.request_models.request_base import MenuRequest
from src.api.response_models.menu_response import MenuInfResponse, MenuSummaryResponse
from src.services.menus_service import MenuService

menu_router = APIRouter(prefix='/menus', tags=['Menu'])


@cbv(menu_router)
class MenuCBV:
    """Class that combines requests for a Menu model."""

    __menu_service: MenuService = Depends()

    @menu_router.post(
        '/',
        summary='Create a new menu',
        description='To create a menu, send a POST request with JSON data containing the "title" '
        'and "description" fields in string format.',
        response_model=MenuInfResponse,
        status_code=HTTPStatus.CREATED,
        response_description='The created menu',
    )
    async def create_menu_router(self, schema: MenuRequest) -> MenuInfResponse:
        return await self.__menu_service.create_menu(schema)

    @menu_router.get(
        '/{menu_id}',
        summary='Get a menu by ID',
        description='To retrieve a menu, send a GET request with the menu_id parameter in the URL.',
        response_model=MenuInfResponse,
        status_code=HTTPStatus.OK,
        response_description='The requested menu',
    )
    async def get_menu_router(
        self,
        menu_id: UUID4 = Path(
            ..., description='The ID of the menu to retrieve'
        ),
    ) -> MenuInfResponse:
        return await self.__menu_service.get_menu(menu_id)

    @menu_router.patch(
        '/{menu_id}',
        summary='Update a menu by ID',
        description='To update a menu, send a PATCH request with the menu_id parameter in the URL '
        'and JSON data containing the "title" and "description" fields in string format in the request body.',
        response_model=MenuInfResponse,
        status_code=HTTPStatus.OK,
        response_description='The menu with changes',
    )
    async def update_menu_router(
        self,
        schema: MenuRequest,
        menu_id: UUID4 = Path(..., description='The ID of the menu to update'),
    ) -> MenuInfResponse:
        return await self.__menu_service.update_menu(menu_id, schema)

    @menu_router.delete(
        '/{menu_id}',
        summary='Delete a menu by ID',
        description='To delete a menu, send a DELETE request with the menu_id parameter in the URL.',
        response_model=None,
        status_code=HTTPStatus.OK,
        response_description='Returns an empty JSON with status code 200 if deletion was successful',
    )
    async def delete_menu_router(
        self,
        menu_id: UUID4 = Path(..., description='The ID of the menu to delete'),
    ) -> JSONResponse:
        return await self.__menu_service.delete_menu(menu_id)

    @menu_router.get(
        '/',
        summary='Get a list of available menus',
        description='To retrieve menus, send a GET request to the "menus" URL path.',
        response_model=list[MenuInfResponse],
        status_code=HTTPStatus.OK,
        response_description='Returns a list of menus, or an empty list if no menus have been created',
    )
    async def get_menus_router(self) -> list[MenuInfResponse]:
        return await self.__menu_service.get_menus()

    @menu_router.get(
        '/menus_info/',
        summary='Get full info about menus including dishes,submenus',
        description='To get full info send a GET request, '
        'the response comes according to the changes in the administrators excel file',
        response_model=list[MenuSummaryResponse],
        status_code=HTTPStatus.OK,
        response_description='Summary_menus_info',
    )
    async def get_all_info_router(self) -> list[MenuSummaryResponse]:
        return await self.__menu_service.full_menus()
