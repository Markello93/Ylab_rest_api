from http import HTTPStatus
from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi_restful.cbv import cbv
from fastapi.responses import JSONResponse

from src.api.request_models.request_base import MenuRequest
from src.api.response_models.menu_response import MenuResponse, MenuInfResponse
from src.services.menus_service import MenuService

menu_router = APIRouter(prefix="/menus", tags=["Menu"])


@cbv(menu_router)
class MenuCBV:
    """Class that combines requests for a Menu model."""

    __menu_service: MenuService = Depends()

    @menu_router.post(
        "/", response_model=MenuResponse, status_code=HTTPStatus.CREATED
    )
    async def create_menu_router(self, schema: MenuRequest):
        return await self.__menu_service.create_menu(schema)

    @menu_router.get(
        "/{menu_id}",
        response_model=MenuInfResponse,
        status_code=HTTPStatus.OK,
    )
    async def get_menu_router(self, menu_id: UUID):
        return await self.__menu_service.get_menu(menu_id)

    @menu_router.patch(
        "/{menu_id}", response_model=MenuResponse, status_code=HTTPStatus.OK
    )
    async def update_menu_router(self, menu_id: UUID, schema: MenuRequest):
        return await self.__menu_service.update_menu(menu_id, schema)

    @menu_router.delete(
        "/{menu_id}", response_model=None, status_code=HTTPStatus.OK
    )
    async def delete_menu_router(self, menu_id: UUID):
        await self.__menu_service.delete_menu(menu_id)
        return JSONResponse(content={}, status_code=HTTPStatus.OK)

    @menu_router.get(
        "/", response_model=List[MenuInfResponse], status_code=HTTPStatus.OK
    )
    async def get_menus_router(self):
        return await self.__menu_service.get_menus()
