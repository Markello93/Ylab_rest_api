from http import HTTPStatus

from fastapi import APIRouter, Depends
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
        '/', response_model=SubmenuInfoResponse, status_code=HTTPStatus.CREATED
    )
    async def create_submenu_router(self, menu_id: UUID4, schema: MenuRequest):
        return await self.__submenu_service.create_submenu(menu_id, schema)

    @submenus_router.get(
        '/{submenu_id}',
        response_model=SubmenuInfoResponse,
        status_code=HTTPStatus.OK,
    )
    async def get_submenu_router(self, menu_id: UUID4, submenu_id: UUID4):
        return await self.__submenu_service.get_submenu(menu_id, submenu_id)

    @submenus_router.patch(
        '/{submenu_id}',
        response_model=SubmenuInfoResponse,
        status_code=HTTPStatus.OK,
    )
    async def update_submenu_router(
        self, submenu_id: UUID4, schema: MenuRequest
    ):
        return await self.__submenu_service.update_submenu(submenu_id, schema)

    @submenus_router.delete('/{submenu_id}', response_model=None, status_code=HTTPStatus.OK
                            )
    async def delete_submenu_router(self, menu_id: UUID4, submenu_id: UUID4):
        await self.__submenu_service.delete_submenu(menu_id, submenu_id)
        return JSONResponse(content={}, status_code=HTTPStatus.OK)

    @submenus_router.get('/', response_model=list[SubmenuInfoResponse])
    async def get_submenus_router(self, menu_id: UUID4):
        return await self.__submenu_service.list_all_submenus(menu_id)
