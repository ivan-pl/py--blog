from src.db import Base, Session, SessionType, create_user, create_post, User, Post, InvalidUserName
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
    password = "1234"
    assert session.query(User).filter_by(name=username).first() is None
    user = create_user(session, username, password)
    assert session.query(User).filter_by(name=username).one() == user
    with raises(InvalidUserName):
        create_user(session, username, password)

    username2 = "Pavel"
    user2 = create_user(session, username2, password)
    assert session.query(User).filter_by(name=username2).one() == user2
    assert session.query(User).count() == 2


def test_create_post(session):
    user = create_user(session, "Ivan", "1234")
    assert session.query(Post).count() == 0
    post = create_post(session, user, "Title", "Lorem ipsum")
    assert session.query(Post).filter_by(author_id=user.id).one() == post
