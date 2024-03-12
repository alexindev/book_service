from sqlalchemy import select, func

from .connect import async_session
from .models import User, Department, Book, UserBook


class BaseCRUD:
    """ Базовые методы для добавления и удаления записей """
    model = None

    @classmethod
    async def add_data(cls, data: str, ) -> str:
        """ Добавить запись """

        async with async_session() as session:
            # Проверяем, существует ли запись в таким именем

            query = select(cls.model).filter_by(name=data)
            result = await session.execute(query)
            exists_already = result.scalar()

            if exists_already:
                return "Запись с таким названием уже существует"
            else:
                # создаем новую запись
                new_row = cls.model(name=data)
                session.add(new_row)
                await session.commit()
                return "Новая запись успешно добавлена"

    @classmethod
    async def del_data(cls, data_id: int) -> str:
        """ Удалить запись """
        async with async_session() as session:
            result = await session.execute(select(cls.model).filter_by(id=data_id))
            row_to_delete = result.scalars().first()

            # удалим запись, если нашли запись
            if row_to_delete:
                await session.delete(row_to_delete)
                await session.commit()
                return f"Запись с id: {data_id} удалена"

            # иначе выводим сообщение
            else:
                return f"Записи с id: {data_id} не существует"


class DepartmentProcess:
    """ Методы для работы с отделом """
    @classmethod
    async def get_departments(cls):
        """ Получить все отделы """
        async with async_session() as session:
            query = select(Department)
            depart = await session.execute(query)
            return depart.scalars().all()


class BookProcess:
    """ Методы для работы с книгами """
    @classmethod
    async def get_filtered_books(cls, author, year, department, amount):
        """ Получить книги по фильтрам """
        async with async_session() as session:
            query = select(Book)

            # Применяем фильтры, если они были указаны
            if department is not None:
                query = query.join(Department).filter(Department.name == department)
            if author is not None:
                query = query.filter_by(author=author)
            if year is not None:
                query = query.filter_by(year=year)
            if amount is not None:
                query = query.filter_by(amount=amount)
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def recieve_book(cls, user_id: int, book_id: int, quantity: int):
        """ Выдать книгу пользователю и обновить количество """
        async with async_session() as session:
            # Получаем книгу
            book = await session.get(Book, book_id)
            if book and book.amount >= quantity:
                # Уменьшаем количество доступных книг
                book.amount -= quantity

                # Проверяем, существует ли уже запись для данного пользователя и книги
                existing_entry = await session.execute(
                    select(UserBook).filter(
                        UserBook.user_id == user_id,
                        UserBook.book_id == book_id
                    )
                )
                existing_entry = existing_entry.scalars().first()

                if existing_entry:
                    # Если запись существует, обновляем количество
                    if existing_entry.amount is None:
                        existing_entry.amount = quantity
                    else:
                        existing_entry.amount += quantity
                else:
                    # Если записи нет, создаем новую
                    new_entry = UserBook(
                        user_id=user_id,
                        book_id=book_id,
                        amount=quantity
                    )
                    session.add(new_entry)

                await session.commit()
                return f"Посетителю выдали книгу {book.name}"
            else:
                return "Недостаточно книг или книга не найдена"

    @classmethod
    async def return_book(cls, user_id: int, book_id: int, quantity: int):
        """Вернуть книгу от пользователя и обновить количество"""
        async with async_session() as session:
            user_book_entry = await session.execute(
                select(UserBook).where(
                    UserBook.user_id == user_id,
                    UserBook.book_id == book_id
                )
            )
            user_book_entry = user_book_entry.scalars().first()

            book = await session.get(Book, book_id)

            if user_book_entry and book:
                if user_book_entry.amount >= quantity:
                    user_book_entry.amount -= quantity

                    if user_book_entry.amount == 0:
                        await session.delete(user_book_entry)

                    book.amount += quantity

                    await session.commit()
                    return f"Вернули книгу {book.name} от пользователя."
                else:
                    return "Пользователь пытается вернуть больше книг, чем взял."
            else:
                return "Запись о взятой книге или сама книга не найдены."


class UserProcess:
    """ Методы для работы с пользователями """
    @classmethod
    async def get_users(cls):
        """ Посетители с количеством книг """
        async with async_session() as session:
            query = select(
                User.name,
                func.count(UserBook.book_id).label("books_count")
            ).join(
                UserBook, User.id == UserBook.user_id, isouter=True
            ).group_by(
                User.name
            )

            result = await session.execute(query)
            users_with_books = result.all()
            return users_with_books

    @classmethod
    async def get_user_books(cls, user_id: int):
        # Получаем пользователя и его книги
        async with async_session() as session:
            query = select(
                Book.name.label('book_name'),
                Book.author,
                Book.year,
                Department.name.label('department')
            ).join(
                UserBook, UserBook.book_id == Book.id
            ).join(
                Department, Department.id == Book.depart_id
            ).filter(
                UserBook.user_id == user_id
            )

            result = await session.execute(query)
            books = result.mappings().all()
            return books


class DepartmentCRUD(BaseCRUD):
    model = Department


class UserCRUD(BaseCRUD):
    model = User
