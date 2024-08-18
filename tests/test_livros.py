from http import HTTPStatus

from madr.schemas import LivroDB


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
