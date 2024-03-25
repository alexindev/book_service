from fastapi import APIRouter

from app.db.processing import UserCRUD, UserProcess
from app.schemas import SUsersWithBooks
from app.schemas import SUserInfo

router = APIRouter(tags=["Пользователи"])


@router.delete('/del_user')
async def del_department(user_id: int) -> str:
    """ Удалить посетителя по его id """
    return await UserCRUD.del_data(user_id)


@router.post('/add_user')
async def add_department(username: str) -> str:
    """ Добавить нового посетеля """
    return await UserCRUD.add_data(username)


@router.get('/get_users')
async def get_users() -> list[SUsersWithBooks]:
    """ Получить всех посетителей с количеством книг """
    return await UserProcess.get_users()


@router.get('/user_info')
async def user_info(user_id: int) -> list[SUserInfo]:
    """ Подробная информация по пользователю """
    return await UserProcess.get_user_books(user_id)
