from http import HTTPStatus

from fastapi import APIRouter, Depends, Path
from fastapi.responses import JSONResponse
from fastapi_restful.cbv import cbv
from pydantic import UUID4

from src.api.request_models.request_base import MenuRequest
from src.api.response_models.submenu_response import SubmenuInfoResponse
from src.services.submenus_service import SubmenuService

submenus_router = APIRouter(
    prefix='/menus/{menu_id}/submenus', tags=['Submenu']
)


@cbv(submenus_router)
class SubmenuCBV:
    """Class that combines requests for a Submenu model."""

    __submenu_service: SubmenuService = Depends()

    @submenus_router.post(
        '/',
        summary='Create a new submenu',
        description='To create a submenu, send a POST request with the "menu_id" parameter in the URL '
        'and JSON data containing the "title" and "description" fields in string format.',
        response_model=SubmenuInfoResponse,
        status_code=HTTPStatus.CREATED,
    )
    async def create_submenu_router(
        self, menu_id: UUID4, schema: MenuRequest
    ) -> SubmenuInfoResponse:
        return await self.__submenu_service.create_submenu(menu_id, schema)

    @submenus_router.get(
        '/{submenu_id}',
        summary='Get a submenu by ID',
        description='To retrieve a submenu, send a GET request with the "menu_id" and "submenu_id" parameters in the URL.',
        response_model=SubmenuInfoResponse,
        status_code=HTTPStatus.OK,
        response_description='The requested submenu',
    )
    async def get_submenu_router(
        self,
        menu_id: UUID4 = Path(
            ..., description='The ID of the menu related to this submenu'
        ),
        submenu_id: UUID4 = Path(
            ..., description='The ID of the menu to retrieve'
        ),
    ) -> SubmenuInfoResponse:
        return await self.__submenu_service.get_submenu(menu_id, submenu_id)

    @submenus_router.patch(
        '/{submenu_id}',
        summary='Update a submenu by ID',
        description='To update a submenu, send a PATCH request with the "menu_id" and "submenu_id" parameters in the URL '
        'and JSON data containing the "title" and "description" fields in string format in the request body.',
        response_model=SubmenuInfoResponse,
        status_code=HTTPStatus.OK,
        response_description='The submenu with changes',
    )
    async def update_submenu_router(
        self,
        schema: MenuRequest,
        submenu_id: UUID4 = Path(
            ..., description='The ID of the submenu to update'
        ),
    ) -> SubmenuInfoResponse:
        return await self.__submenu_service.update_submenu(submenu_id, schema)

    @submenus_router.delete(
        '/{submenu_id}',
        summary='Delete a submenu by ID',
        description='To delete a submenu, send a DELETE request with the "menu_id" and "submenu_id" parameters in the URL.',
        response_model=None,
        status_code=HTTPStatus.OK,
        response_description='Returns an empty JSON with status code 200 if deletion was successful',
    )
    async def delete_submenu_router(
        self,
        menu_id: UUID4 = Path(
            ..., description='The ID of the menu related to this submenu'
        ),
        submenu_id: UUID4 = Path(
            ..., description='The ID of the submenu to delete'
        ),
    ) -> JSONResponse:
        return await self.__submenu_service.delete_submenu(menu_id, submenu_id)

    @submenus_router.get(
        '/',
        summary='Get a list of available submenus',
        description='To retrieve submenus, send a GET request to the "submenus" URL path.',
        response_model=list[SubmenuInfoResponse],
        response_description='Returns a list of submenus, or an empty list if no submenus have been created',
    )
    async def get_submenus_router(
        self, menu_id: UUID4
    ) -> list[SubmenuInfoResponse]:
        return await self.__submenu_service.get_submenus(menu_id)
