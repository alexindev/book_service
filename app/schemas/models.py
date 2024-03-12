from pydantic import BaseModel


class SDepartment(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class SBook(BaseModel):
    id: int
    name: str
    author: str
    year: int
    amount: int
    depart_id: int

    class Config:
        from_attributes = True
