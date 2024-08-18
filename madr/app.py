from http import HTTPStatus

from fastapi import FastAPI

from madr.routers import auth, livros, romancistas, users
from madr.schemas import Message

app = FastAPI()

app.include_router(users.router)
app.include_router(livros.router)
app.include_router(romancistas.router)
app.include_router(auth.router)


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'Olá Mundo!'}
