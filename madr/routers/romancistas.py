from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from madr.database import get_session
from madr.models import Romancista
from madr.schemas import Message, RomancistaDB, RomancistaList, RomancistaSchema

router = APIRouter(prefix='/romancistas', tags=['romancistas'])
Session = Annotated[Session, Depends(get_session)]


@router.post('/', status_code=HTTPStatus.CREATED, response_model=RomancistaDB)
def create_romancista(romancista: RomancistaSchema, session: Session):
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


@router.get('/', response_model=RomancistaList)
def read_romancista(session: Session, skip: int = 0, limit: int = 100):
    romancistas = session.scalars(select(Romancista).offset(skip).limit(limit)).all()
    return {'romancistas': romancistas}


@router.put('/{romancista_id}', response_model=RomancistaDB)
def update_romancistta(romancista_id: int, romancista: RomancistaSchema, session: Session):
    db_romancista = session.scalar(select(Romancista).where(Romancista.id == romancista_id))
    if not db_romancista:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Romancista não encontrado')

    db_romancista.nome = romancista.nome
    session.commit()
    session.refresh(db_romancista)

    return db_romancista


@router.delete('/{romancista_id}', response_model=Message)
def delete_romancista(romancista_id: int, session: Session):
    db_romancista = session.scalar(select(Romancista).where(Romancista.id == romancista_id))

    if not db_romancista:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Romancista não encontrado')

    session.delete(db_romancista)
    session.commit()
    return {'message': 'Romancista deletado no MADR'}
