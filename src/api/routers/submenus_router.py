from http import HTTPStatus
from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi_restful.cbv import cbv
from fastapi.responses import JSONResponse

from src.api.request_models.request_base import MenuRequest
from src.api.response_models.submenu_response import (
    SubmenuInfoResponse,
    SubmenuResponse,
)
from src.services.submenus_service import SubmenuService

submenus_router = APIRouter(
    prefix="/menus/{menu_id}/submenus", tags=["Submenu"]
)


@cbv(submenus_router)
class SubmenuCBV:
    """Class that combines requests for a Submenu model."""

    __submenu_service: SubmenuService = Depends()

    @submenus_router.post(
        "/", response_model=SubmenuResponse, status_code=HTTPStatus.CREATED
    )
    async def create_submenu_router(self, menu_id: UUID, schema: MenuRequest):
        return await self.__submenu_service.create_submenu(menu_id, schema)

    @submenus_router.get(
        "/{submenu_id}",
        response_model=SubmenuInfoResponse,
        status_code=HTTPStatus.OK,
    )
    async def get_submenu_router(self, submenu_id: UUID):
        submenu = await self.__submenu_service.get_submenu(submenu_id)

        return submenu

    @submenus_router.patch(
        "/{submenu_id}",
        response_model=SubmenuResponse,
        status_code=HTTPStatus.OK,
    )
    async def update_submenu_router(
        self, submenu_id: UUID, schema: MenuRequest
    ):
        return await self.__submenu_service.update_submenu(submenu_id, schema)

    @submenus_router.delete("/{submenu_id}", status_code=HTTPStatus.OK)
    async def delete_menu_router(self, submenu_id: UUID):
        await self.__submenu_service.delete_submenu(submenu_id)
        return JSONResponse(content={}, status_code=HTTPStatus.OK)

    @submenus_router.get("/", response_model=List[SubmenuInfoResponse])
    async def get_submenus_router(self, menu_id: UUID):
        return await self.__submenu_service.list_all_submenus(menu_id)
