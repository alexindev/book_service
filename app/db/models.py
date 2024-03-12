from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, DeclarativeBase


class Base(DeclarativeBase):
    id = Column(Integer, primary_key=True)


class User(Base):
    __tablename__ = 'user'
    name = Column(String, nullable=False)
    books = relationship('UserBook', back_populates='user')

    def __repr__(self):
        return f"<User(id={self.id}, user_name={self.name})>"


class UserBook(Base):
    __tablename__ = 'user_book'
    book_id = Column(ForeignKey('book.id'))
    user_id = Column(ForeignKey('user.id'))
    amount = Column(Integer, nullable=True)
    user = relationship('User', back_populates='books')
    book = relationship('Book', back_populates='borrowers')

    def __repr__(self):
        return f"<UserBook(id={self.id}, book_id={self.book_id}), user_id={self.user_id}>"


class Book(Base):
    __tablename__ = 'book'
    name = Column(String, nullable=False)
    author = Column(String, nullable=False)
    year = Column(Integer, nullable=False)
    amount = Column(Integer, nullable=False)
    depart_id = Column(ForeignKey('department.id'))
    department = relationship('Department', back_populates='books')
    borrowers = relationship('UserBook', back_populates='book')

    def __repr__(self):
        return (f"Book(id={self.id}, book_name='{self.name}', author='{self.author}', year={self.year}, "
                f"depart_id={self.depart_id}, amount={self.amount})>")


class Department(Base):
    __tablename__ = 'department'
    name = Column(String, nullable=False)
    books = relationship('Book', back_populates='department')

    def __repr__(self):
        return f"Department(id={self.id}, depart_name='{self.name}'>"
