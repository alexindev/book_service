from typing import Optional

from fastapi import APIRouter

from app.db.processing import BookProcess
from app.schemas import SBook

router = APIRouter(tags=["Книги"])


@router.get('/books')
async def get_books(
    author: Optional[str] = None,
    year: Optional[int] = None,
    department: Optional[str] = None,
    amount: Optional[int] = None
) -> list[SBook]:
    """ Получить список книг по фильтрам """
    return await BookProcess.get_filtered_books(author, year, department, amount)


@router.put('/recieve_book')
async def recieve_book(user_id: int, book_id: int, quantity: int) -> str:
    """ Выдать книгу посетителю """
    return await BookProcess.recieve_book(user_id, book_id, quantity)


@router.put('/return_book')
async def return_book(user_id: int, book_id: int, quantity: int) -> str:
    """ Получить книгу от посетителя """
    return await BookProcess.return_book(user_id, book_id, quantity)
