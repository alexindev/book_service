from pydantic import BaseModel


class SUsersWithBooks(BaseModel):
    name: str
    books_count: int

    class Config:
        from_attributes = True


class SUserInfo(BaseModel):
    book_name: str
    author: str
    year: int
    department: str

    class Config:
        from_attributes = True
