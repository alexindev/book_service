from fastapi import FastAPI

from app.routers import user, depart, book

app = FastAPI()

app.include_router(user)
app.include_router(depart)
app.include_router(book)
