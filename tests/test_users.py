from http import HTTPStatus

from madr.schemas import UserPublic


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


def test_update_user(client, user, token):
    response = client.put(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
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
        'id': user.id,
    }


def test_delete_user(client, user, token):
    response = client.delete(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Conta deletada com sucesso'}


def test_delete_wrong_user(client, user, token):
    response = client.delete(
        f'/users/{user.id + 1}',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'Not enough permissions'}
