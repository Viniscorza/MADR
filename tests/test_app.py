from http import HTTPStatus

from madr.schemas import LivroDB, RomancistaDB, UserPublic


def test_root_deve_retornar_ok_e_ola_mundo(client):
    response = client.get('/')  # Act

    assert response.status_code == HTTPStatus.OK  # Assert
    assert response.json() == {'message': 'Olá Mundo!'}  # Assert


def test_create_user(client):
    response = client.post(
        '/users/',
        json={
            'username': 'testusername',
            'email': 'email@email.com',
            'password': 'password',
        },
    )

    # voltou o status code correto?
    assert response.status_code == HTTPStatus.CREATED
    # Validar UserPublic
    assert response.json() == {
        'username': 'testusername',
        'email': 'email@email.com',
        'id': 1,
    }


def test_read_users(client):
    response = client.get('/users')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': []}


def test_read_users_with_users(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get('/users/')
    assert response.json() == {'users': [user_schema]}


def test_update_user(client, user):
    response = client.put(
        '/users/1',
        json={
            'password': 'novasenha',
            'username': 'testusername2',
            'email': 'email@email.com',
        },
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'testusername2',
        'email': 'email@email.com',
        'id': 1,
    }


def test_delete_user(client, user):
    response = client.delete('/users/1')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Conta deletada com sucesso'}


def test_create_livro(client):
    response = client.post(
        '/livros/',
        json={
            'ano': '1980',
            'titulo': 'pega na minha que eu entro na sua',
            'id_romancista': 1,
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'id': 1,
        'ano': '1980',
        'titulo': 'pega na minha que eu entro na sua',
        'id_romancista': 1,
    }


def test_read_livros(client):
    response = client.get('/livros/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'livros': []}


def test_read_livros_with_livros(client, livro):
    livro_schema = LivroDB.model_validate(livro).model_dump()
    response = client.get('/livros/')
    assert response.json() == {'livros': [livro_schema]}


def test_update_livro(client, livro):
    response = client.put(
        '/livros/1',
        json={
            'ano': '1990',
            'titulo': 'novo titulo',
            'id_romancista': 2,
        },
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'ano': '1990',
        'titulo': 'novo titulo',
        'id_romancista': 2,
        'id': 1,
    }


def test_delete_livro(client, livro):
    response = client.delete('/livros/1')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Livro deletado no MADR'}


def test_create_romancista(client):
    response = client.post('/romancistas/', json={'nome': 'vini scrz'})

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'id': 1,
        'nome': 'vini scrz',
    }


def test_read_romancista(client):
    response = client.get('/romancistas/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'romancistas': []}


def test_read_romancistas_with_romancistas(client, romancista):
    romancista_schema = RomancistaDB.model_validate(romancista).model_dump()
    response = client.get('/romancistas/')
    assert response.json() == {'romancistas': [romancista_schema]}


def test_update_romancista(client, romancista):
    response = client.put(
        '/romancistas/1',
        json={
            'nome': 'tirso tiriço',
        },
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'nome': 'tirso tiriço',
        'id': 1,
    }


def test_delete_romancista(client, romancista):
    response = client.delete('/romancistas/1')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Romancista deletado no MADR'}
