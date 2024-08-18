import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from madr.app import app
from madr.database import get_session
from madr.models import Livro, Romancista, User, table_registry
from madr.security import get_password_hash


@pytest.fixture
def session():
    engine = create_engine(
        'sqlite:///:memory:',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )
    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    table_registry.metadata.drop_all(engine)


@pytest.fixture
def client(session):
    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override
        yield client

    app.dependency_overrides.clear()


#  def client():
#  return TestClient(app)


@pytest.fixture
def user(session):
    user = User(
        username='Teste',
        email='teste@test.com',
        password=get_password_hash('testtest'),
    )
    session.add(user)
    session.commit()
    session.refresh(user)

    user.clean_password = 'testtest'

    return user


@pytest.fixture
def livro(session):
    livro = Livro(ano='2024', titulo='Lula e seu bando se foderam', id_romancista=0)
    session.add(livro)
    session.commit()
    session.refresh(livro)

    return livro


@pytest.fixture
def romancista(session):
    romancista = Romancista(nome='Clarisse')
    session.add(romancista)
    session.commit()
    session.refresh(romancista)

    return romancista


@pytest.fixture
def token(client, user):
    response = client.post(
        '/auth/token',
        data={'username': user.email, 'password': user.clean_password},
    )
    return response.json()['access_token']
