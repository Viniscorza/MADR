from http import HTTPStatus

from madr.schemas import RomancistaDB


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
