from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from madr.database import get_session
from madr.models import Livro
from madr.schemas import LivroDB, LivroList, LivroSchema, Message

router = APIRouter(prefix='/livros', tags=['livros'])
Session = Annotated[Session, Depends(get_session)]


@router.post('/', status_code=HTTPStatus.CREATED, response_model=LivroDB)
def create_livro(livro: LivroSchema, session: Session):
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


@router.get('/', response_model=LivroList)
def read_livro(session: Session, skip: int = 0, limit: int = 100):
    livros = session.scalars(select(Livro).offset(skip).limit(limit)).all()
    return {'livros': livros}


@router.put('/{livro_id}', response_model=LivroDB)
def update_livro(livro_id: int, livro: LivroSchema, session: Session):
    db_livro = session.scalar(select(Livro).where(Livro.id == livro_id))
    if not db_livro:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Livro não encontrado')

    db_livro.ano = livro.ano
    db_livro.titulo = livro.titulo
    db_livro.id_romancista = livro.id_romancista
    session.commit()
    session.refresh(db_livro)

    return db_livro


@router.delete('/{livro_id}', response_model=Message)
def delete_livro(livro_id: int, session: Session):
    db_livro = session.scalar(select(Livro).where(Livro.id == livro_id))

    if not db_livro:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Livro não encontrado')

    session.delete(db_livro)
    session.commit()

    return {'message': 'Livro deletado no MADR'}
