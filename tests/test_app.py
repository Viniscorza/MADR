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
