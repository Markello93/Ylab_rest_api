from http import HTTPStatus
from typing import List, Optional
from uuid import UUID
from fastapi.responses import JSONResponse
from fastapi import APIRouter, Depends
from fastapi_restful.cbv import cbv

from src.api.request_models.request_base import DishRequest
from src.api.response_models.dish_response import DishResponse
from src.services.dishes_service import DishService

dishes_router = APIRouter(
    prefix="/menus/{menu_id}/submenus/{submenu_id}/dishes", tags=["Dishes"]
)


@cbv(dishes_router)
class DishCBV:
    """Class that combines requests for a Dish model."""

    __dish_service: DishService = Depends()

    @dishes_router.post(
        "/",
        response_model=Optional[DishResponse],
        status_code=HTTPStatus.CREATED,
    )
    async def create_dish_router(self, submenu_id: UUID, schema: DishRequest):
        return await self.__dish_service.create_dish(submenu_id, schema)

    @dishes_router.get("/{dish_id}", response_model=DishResponse)
    async def get_dish_router(self, dish_id: UUID):
        return await self.__dish_service.get_dish(dish_id)

    @dishes_router.patch(
        "/{dish_id}",
        response_model=Optional[DishResponse],
        status_code=HTTPStatus.OK,
    )
    async def update_dish_router(
        self,
        dish_id: UUID,
        schema: DishRequest,
    ):
        return await self.__dish_service.update_dish(dish_id, schema)

    @dishes_router.delete(
        "/{dish_id}", response_model=None, status_code=HTTPStatus.OK
    )
    async def delete_dish_router(self, dish_id: UUID):
        await self.__dish_service.delete_dish(dish_id)
        return JSONResponse(content={}, status_code=HTTPStatus.OK)

    @dishes_router.get(
        "/", response_model=List[DishResponse], status_code=HTTPStatus.OK
    )
    async def get_dishes_router(self, menu_id: UUID, submenu_id: UUID):
        return await self.__dish_service.get_dishes(menu_id, submenu_id)
