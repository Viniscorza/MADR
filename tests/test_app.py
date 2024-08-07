from http import HTTPStatus


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
    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'users': [
            {
                'username': 'testusername',
                'email': 'email@email.com',
                'id': 1,
            }
        ]
    }


def test_update_user(client):
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


def test_delete_user(client):
    response = client.delete('/users/1')

    # assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted'}


def test_create_livro(livro):
    response = livro.post(
        '/livros/',
        json={
            'id': 1,
            'ano': '1980',
            'titulo': 'pega na minha que eu entro na sua',
            'id_romancista': 1,
        },
    )

    # voltou o status code correto?
    assert response.status_code == HTTPStatus.CREATED
    # Validar UserPublic
    assert response.json() == {
        'id': 1,
        'ano': '1980',
        'titulo': 'pega na minha que eu entro na sua',
        'id_romancista': 1,
    }


def test_read_livros(livro):
    response = livro.get('/livros/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'livros': [
            {
                'id': 1,
                'ano': '1980',
                'titulo': 'pega na minha que eu entro na sua',
                'id_romancista': 1,
            }
        ]
    }


def test_update_livro(livro):
    response = livro.put(
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


def test_delete_livro(livro):
    response = livro.delete('/livros/1')

    # assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Livro deletado'}


def test_create_romancista(romancista):
    response = romancista.post(
        '/romancistas/',
        json={
            'id': 1,
            'nome': 'vini scrz',
            'livros': 'varios',
        },
    )

    # voltou o status code correto?
    assert response.status_code == HTTPStatus.CREATED
    # Validar UserPublic
    assert response.json() == {
        'id': 1,
        'nome': 'vini scrz',
        'livros': 'varios',
    }


def test_read_romancista(romancista):
    response = romancista.get('/romancistas/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'romancistas': [
            {
                'id': 1,
                'nome': 'vini scrz',
                'livros': 'varios',
            }
        ]
    }


def test_update_romancista(romancista):
    response = romancista.put(
        '/romancistas/1',
        json={
            'nome': 'tirso tiriço',
            'livros': 'muitos',
            'id': 1,
        },
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'nome': 'tirso tiriço',
        'livros': 'muitos',
        'id': 1,
    }


def test_delete_romancista(romancista):
    response = romancista.delete('/romancistas/1')

    # assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Romancista deletado'}
