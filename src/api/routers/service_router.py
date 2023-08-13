from fastapi import APIRouter, Depends, HTTPException

from src.services.dishes_service import DishService
from src.services.menus_service import MenuService
from src.services.submenus_service import SubmenuService
from src.tasks.excel_to_db import ExcelParser

parser_router = APIRouter(prefix='/parser', tags=['Parser'])


@parser_router.post(
    '/parse-excel',
    summary='Parse Excel and load data to the database',
    description='Parse the Excel file and load its data into the database.',
    response_description='Data parsing and loading result',
)
async def parse_excel(
    menu_service: MenuService = Depends(),
    submenu_service: SubmenuService = Depends(),
    dish_service: DishService = Depends()
):
    try:
        excel_parser = ExcelParser(menu_service, submenu_service, dish_service)
        await excel_parser.parse_excel_and_load_to_db()
        return {'message': 'Excel data parsed and loaded successfully'}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
