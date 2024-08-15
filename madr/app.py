from http import HTTPStatus

from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session

from madr.database import get_session
from madr.models import Livro, Romancista, User
from madr.schemas import (
    LivroDB,
    LivroList,
    LivroSchema,
    Message,
    RomancistaDB,
    RomancistaList,
    RomancistaSchema,
    Token,
    UserList,
    UserPublic,
    UserSchema,
)
from madr.security import (
    create_access_token,
    get_current_user,
    get_password_hash,
    verify_password,
)

# from madr.routers import auth, todos, users

# from fastapi.responses import HTMLResponse

app = FastAPI()

# app.include_router(users.router)
# app.include_router(auth.router)
# app.include_router(todos.router)


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'Olá Mundo!'}


@app.post('/users/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema, session: Session = Depends(get_session)):
    db_user = session.scalar(
        select(User).where((User.username == user.username) | (User.email == user.email))
    )

    if db_user:
        if db_user.username == user.username:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Username already exists',
            )
        elif db_user.email == user.email:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Email already exists',
            )

    hashed_password = get_password_hash(user.password)

    db_user = User(
        username=user.username,
        password=hashed_password,
        email=user.email,
    )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@app.get('/users/', response_model=UserList)
def read_users(skip: int = 0, limit: int = 100, session: Session = Depends(get_session)):
    users = session.scalars(select(User).offset(skip).limit(limit)).all()
    return {'users': users}


@app.put('/users/{user_id}', response_model=UserPublic)
def update_user(
    user_id: int,
    user: UserSchema,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    if current_user.id != user_id:
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail='Not enough permissions')

    current_user.username = user.username
    current_user.password = get_password_hash(user.password)
    current_user.email = user.email
    session.commit()
    session.refresh(current_user)

    return current_user


@app.delete('/users/{user_id}', response_model=Message)
def delete_user(
    user_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    if current_user.id != user_id:
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail='Not enough permissions')

    session.delete(current_user)
    session.commit()

    return {'message': 'Conta deletada com sucesso'}


@app.post('/livros/', status_code=HTTPStatus.CREATED, response_model=LivroDB)
def create_livro(livro: LivroSchema, session: Session = Depends(get_session)):
    db_livro = session.scalar(select(Livro).where(Livro.titulo == livro.titulo))

    if db_livro:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Livro já cadastrado no MADR',
        )

    db_livro = Livro(titulo=livro.titulo, ano=livro.ano, id_romancista=livro.id_romancista)

    session.add(db_livro)
    session.commit()
    session.refresh(db_livro)

    return db_livro


@app.get('/livros/', response_model=LivroList)
def read_livro(skip: int = 0, limit: int = 100, session: Session = Depends(get_session)):
    livros = session.scalars(select(Livro).offset(skip).limit(limit)).all()
    return {'livros': livros}


@app.put('/livros/{livro_id}', response_model=LivroDB)
def update_livro(livro_id: int, livro: LivroSchema, session: Session = Depends(get_session)):
    db_livro = session.scalar(select(Livro).where(Livro.id == livro_id))
    if not db_livro:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Livro não encontrado')

    db_livro.ano = livro.ano
    db_livro.titulo = livro.titulo
    db_livro.id_romancista = livro.id_romancista
    session.commit()
    session.refresh(db_livro)

    return db_livro


@app.delete('/livros/{livro_id}', response_model=Message)
def delete_livro(livro_id: int, session: Session = Depends(get_session)):
    db_livro = session.scalar(select(Livro).where(Livro.id == livro_id))

    if not db_livro:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Livro não encontrado')

    session.delete(db_livro)
    session.commit()

    return {'message': 'Livro deletado no MADR'}


@app.post('/romancistas/', status_code=HTTPStatus.CREATED, response_model=RomancistaDB)
def create_romancista(romancista: RomancistaSchema, session: Session = Depends(get_session)):
    db_romancista = session.scalar(select(Romancista).where(Romancista.nome == romancista.nome))

    if db_romancista:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Romancista já cadastrado no MADR',
        )

    db_romancista = Romancista(nome=romancista.nome)

    session.add(db_romancista)
    session.commit()
    session.refresh(db_romancista)

    return db_romancista


@app.get('/romancistas/', response_model=RomancistaList)
def read_romancista(skip: int = 0, limit: int = 100, session: Session = Depends(get_session)):
    romancistas = session.scalars(select(Romancista).offset(skip).limit(limit)).all()
    return {'romancistas': romancistas}


@app.put('/romancistas/{romancista_id}', response_model=RomancistaDB)
def update_romancistta(
    romancista_id: int, romancista: RomancistaSchema, session: Session = Depends(get_session)
):
    db_romancista = session.scalar(select(Romancista).where(Romancista.id == romancista_id))
    if not db_romancista:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Romancista não encontrado')

    db_romancista.nome = romancista.nome
    session.commit()
    session.refresh(db_romancista)

    return db_romancista


@app.delete('/romancistas/{romancista_id}', response_model=Message)
def delete_romancista(romancista_id: int, session: Session = Depends(get_session)):
    db_romancista = session.scalar(select(Romancista).where(Romancista.id == romancista_id))

    if not db_romancista:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Romancista não encontrado')

    session.delete(db_romancista)
    session.commit()
    return {'message': 'Romancista deletado no MADR'}


@app.post('/token', response_model=Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session),
):
    user = session.scalar(select(User).where(User.email == form_data.username))

    if not user:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail='Incorrect email or password'
        )

    if not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail='Incorrect email or password'
        )

    access_token = create_access_token(data={'sub': user.email})

    return {'access_token': access_token, 'token_type': 'bearer'}
