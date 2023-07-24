from http import HTTPStatus
from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi_restful.cbv import cbv
from fastapi.responses import JSONResponse

from src.api.request_models.request_base import MenuRequest
from src.api.response_models.submenu_response import (
    AllSubmenuResponse,
    SubmenuResponse,
)
from src.core import exceptions
from src.services.submenus_service import SubmenuService

submenus_router = APIRouter(
    prefix="/menus/{menu_id}/submenus", tags=["Submenu"]
)


@cbv(submenus_router)
class SubmenuCBV:
    __submenu_service: SubmenuService = Depends()

    @submenus_router.post(
        "/", response_model=SubmenuResponse, status_code=HTTPStatus.CREATED
    )
    async def create_submenu(self, menu_id: UUID, schema: MenuRequest):
        return await self.__submenu_service.create_submenu(menu_id, schema)

    @submenus_router.get(
        "/{submenu_id}",
        response_model=AllSubmenuResponse,
        status_code=HTTPStatus.OK,
    )
    async def get_submenu(self, menu_id: UUID, submenu_id: UUID):
        submenu = await self.__submenu_service.get_submenu(menu_id, submenu_id)
        if submenu is None:
            raise exceptions.ObjectNotFoundError("submenu")
        submenu_response = AllSubmenuResponse(
            id=submenu.id,
            title=submenu.title,
            menu_id=submenu.menu_id,
            description=submenu.description,
            dishes_count=submenu.num_dishes,
        )
        return submenu_response

    @submenus_router.patch(
        "/{submenu_id}",
        response_model=SubmenuResponse,
        status_code=HTTPStatus.OK,
    )
    async def update_submenu(
        self, menu_id: UUID, submenu_id: UUID, schema: MenuRequest
    ):
        return await self.__submenu_service.update_submenu(
            menu_id, submenu_id, schema
        )

    @submenus_router.delete("/{submenu_id}", status_code=HTTPStatus.OK)
    async def delete_menu(self, menu_id: UUID, submenu_id: UUID):
        await self.__submenu_service.delete_submenu(menu_id, submenu_id)
        return JSONResponse(content={}, status_code=HTTPStatus.OK)

    @submenus_router.get("/", response_model=List[AllSubmenuResponse])
    async def get_submenus(self):
        return await self.__submenu_service.list_all_submenus()
