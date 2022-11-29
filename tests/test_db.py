from src.db import Base, Session, SessionType, create_user, User
from sqlalchemy import select
from pytest import fixture


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
