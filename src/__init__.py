from fastapi import FastAPI

from src.api.routers.dishes_router import dishes_router
from src.api.routers.menus_router import menu_router
from src.api.routers.submenus_router import submenus_router
from src.api.routers.service_router import parser_router
from src.core.settings import settings


def create_app() -> FastAPI:
    app = FastAPI(debug=settings.DEBUG, root_path=settings.RESTO_ROOT_PATH)
    app.include_router(menu_router, prefix='/api/v1')
    app.include_router(submenus_router, prefix='/api/v1')
    app.include_router(dishes_router, prefix='/api/v1')
    app.include_router(parser_router, prefix='/api/v1')

    return app
