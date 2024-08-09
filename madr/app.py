from http import HTTPStatus

from fastapi import FastAPI, HTTPException

from madr.schemas import (
    LivroDB,
    LivroList,
    LivroSchema,
    Message,
    RomancistaDB,
    RomancistaList,
    RomancistaSchema,
    UserDB,
    UserList,
    UserPublic,
    UserSchema,
)

# from madr.routers import auth, todos, users

# from fastapi.responses import HTMLResponse

app = FastAPI()

database = []
datalivro = []
dataromancista = []

# app.include_router(users.router)
# app.include_router(auth.router)
# app.include_router(todos.router)


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'Olá Mundo!'}


@app.post('/users/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema):
    user_with_id = UserDB(**user.model_dump(), id=len(database) + 1)

    database.append(user_with_id)

    return user_with_id


@app.get('/users/', response_model=UserList)
def read_user():
    return {'users': database}


@app.put('/users/{user_id}', response_model=UserPublic)
def update_user(user_id: int, user: UserSchema):
    if user_id < 1 or user_id > len(database):
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='User not found')

    user_with_id = UserDB(**user.model_dump(), id=user_id)

    database[user_id - 1] = user_with_id

    return user_with_id


@app.delete('/users/{user_id}', response_model=Message)
def delete_user(user_id: int):
    if user_id < 1 or user_id > len(database):
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='User not found')

    del database[user_id - 1]

    return {'message': 'Conta deletada com sucesso'}


@app.post('/livros/', status_code=HTTPStatus.CREATED, response_model=LivroDB)
def create_livro(livro: LivroSchema):
    livro_with_id = LivroDB(**livro.model_dump(), id=len(datalivro) + 1)

    datalivro.append(livro_with_id)

    return livro_with_id


@app.get('/livros/', response_model=LivroList)
def read_livro():
    return {'livros': datalivro}


@app.put('/livros/{livro_id}')
def update_livro(livro_id: int, livro: LivroSchema):
    if livro_id < 1 or livro_id > len(datalivro):
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Livro não encontrado')

    livro_with_id = LivroDB(**livro.model_dump(), id=livro_id)

    datalivro[livro_id - 1] = livro_with_id

    return livro_with_id


@app.delete('/livros/{livro_id}', response_model=Message)
def delete_livro(livro_id: int):
    if livro_id < 1 or livro_id > len(datalivro):
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Livro não encontrado')

    del datalivro[livro_id - 1]

    return {'message': 'Livro deletado no MADR'}


@app.post('/romancistas/', status_code=HTTPStatus.CREATED, response_model=RomancistaDB)
def create_romancista(romancista: RomancistaSchema):
    romancista_with_id = RomancistaDB(**romancista.model_dump(), id=len(dataromancista) + 1)

    dataromancista.append(romancista_with_id)

    return romancista_with_id


@app.get('/romancistas/', response_model=RomancistaList)
def read_romancista():
    return {'romancistas': dataromancista}


@app.put('/romancistas/{romancista_id}')
def update_romancistta(romancista_id: int, romancista: RomancistaSchema):
    if romancista_id < 1 or romancista_id > len(dataromancista):
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Romancista não encontrado')

    romancista_with_id = RomancistaDB(**romancista.model_dump(), id=romancista_id)

    dataromancista[romancista_id - 1] = romancista_with_id

    return romancista_with_id


@app.delete('/romancistas/{romancista_id}', response_model=Message)
def delete_romancista(romancista_id: int):
    if romancista_id < 1 or romancista_id > len(dataromancista):
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Romancista não encontrado')

    del dataromancista[romancista_id - 1]

    return {'message': 'Romancista deletado no MADR'}
