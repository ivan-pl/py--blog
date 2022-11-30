from src.db import Base, Session, SessionType, create_user, User, InvalidUserName
from sqlalchemy import select
from pytest import fixture, raises


@fixture
def session() -> SessionType:
    Base.metadata.drop_all()
    Base.metadata.create_all()
    session: SessionType = Session()
    yield session
    session.close()


def test_create_user(session):
    username = "Ivan"
    assert session.query(User).filter_by(name=username).first() is None
    user = create_user(session, username)
    assert session.query(User).filter_by(name=username).one() == user
    with raises(InvalidUserName):
        create_user(session, username)

    username2 = "Pavel"
    user2 = create_user(session, username2)
    assert session.query(User).filter_by(name=username2).one() == user2
    assert session.query(User).count() == 2
