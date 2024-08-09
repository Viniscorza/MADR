from sqlalchemy import select

from madr.models import User


def test_create_user(session):
    new_user = User(username='vini', password='segredo', email='guest@guest.com')
    session.add(new_user)
    session.commit()

    user = session.scalar(select(User).where(User.username == 'vini'))

    assert user.username == 'vini'
