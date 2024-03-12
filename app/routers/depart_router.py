from typing import List

from fastapi import APIRouter
from app.db.processing import DepartmentProcess, DepartmentCRUD
from app.schemas import SDepartment

router = APIRouter(tags=["Отделы"])


@router.post('/get_department')
async def get_department() -> List[SDepartment]:
    """ Получить все отделы """
    return await DepartmentProcess.get_departments()


@router.post('/del_department')
async def del_department(department_id: int) -> str:
    """ Удалить отдел по его id """
    return await DepartmentCRUD.del_data(department_id)


@router.post('/add_department')
async def add_department(department_name: str) -> str:
    """ Добавить новый отдел """
    return await DepartmentCRUD.add_data(department_name)
