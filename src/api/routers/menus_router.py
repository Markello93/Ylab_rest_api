from http import HTTPStatus
from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi_restful.cbv import cbv
from fastapi.responses import JSONResponse

from src.api.request_models.request_base import MenuRequest
from src.api.response_models.menu_response import (
    AllMenuResponse,
    MenuResponse,
    Menu_with_infoResponse,
)
from src.core import exceptions
from src.services.menus_service import MenuService

menu_router = APIRouter(prefix="/menus", tags=["Menu"])


@cbv(menu_router)
class MenuCBV:
    __menu_service: MenuService = Depends()

    @menu_router.post(
        "/", response_model=MenuResponse, status_code=HTTPStatus.CREATED
    )
    async def create_menu(self, schema: MenuRequest):
        return await self.__menu_service.create_menu(schema)

    @menu_router.get(
        "/{menu_id}",
        response_model=Menu_with_infoResponse,
        status_code=HTTPStatus.OK,
    )
    async def get_menu(self, menu_id: UUID):
        menu = await self.__menu_service.get_menu(menu_id)
        if menu is None:
            raise exceptions.ObjectNotFoundError("menu")
        menu_response = Menu_with_infoResponse(
            id=menu.id,
            title=menu.title,
            description=menu.description,
            submenus_count=menu.num_submenus,
            dishes_count=menu.num_dishes,
        )
        return menu_response

    @menu_router.patch(
        "/{menu_id}", response_model=MenuResponse, status_code=HTTPStatus.OK
    )
    async def update_menu(self, menu_id: UUID, schema: MenuRequest):
        return await self.__menu_service.update_menu(menu_id, schema)

    @menu_router.delete(
        "/{menu_id}", response_model=None, status_code=HTTPStatus.OK
    )
    async def delete_menu(self, menu_id: UUID):
        await self.__menu_service.delete_menu(menu_id)
        return JSONResponse(content={}, status_code=HTTPStatus.OK)

    @menu_router.get(
        "/", response_model=List[AllMenuResponse], status_code=HTTPStatus.OK
    )
    async def get_menus(self):
        return await self.__menu_service.get_menus()