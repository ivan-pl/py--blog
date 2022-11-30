from src.db import Base, Session, SessionType, create_user, create_post, create_comment, get_user_posts, get_all_posts, \
    User, Post, \
    Comment, \
    InvalidUserName
from pytest import fixture, raises


@fixture
def session() -> SessionType:
    Base.metadata.drop_all()
    Base.metadata.create_all()
    session: SessionType = Session()
    yield session
    session.close()


@fixture
def user_instance(session) -> User:
    user = create_user(session, "Ivan", "12345")
    return user


@fixture
def post_instance(session, user_instance) -> Post:
    post = create_post(session, author=user_instance, title="Title", content="Some content")
    return post


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


def test_create_post(session, user_instance):
    assert session.query(Post).count() == 0
    post = create_post(session, user_instance, "Title", "Lorem ipsum")
    assert session.query(Post).filter_by(author=user_instance).one() == post


def test_create_comment(session, user_instance, post_instance):
    assert session.query(Comment).count() == 0
    comment = create_comment(session, post_instance, author=user_instance, content="comment 1")
    assert session.query(Comment).filter_by(post=post_instance).one() == comment
    comment2 = create_comment(session, post_instance, author=user_instance, content="comment 2")
    assert session.query(Comment).filter_by(post=post_instance).all() == [comment, comment2]


def test_get_user_posts(session, user_instance, post_instance):
    assert get_user_posts(session, user_instance) == []
    comment1 = create_comment(session, post_instance, author=user_instance, content="comment 1")
    comment2 = create_comment(session, post_instance, author=user_instance, content="comment 2")
    assert get_user_posts(session, user_instance) == [comment1, comment2]


def test_get_all_posts(session, user_instance):
    assert get_all_posts(session) == []
    post1 = create_post(session, author=user_instance, title="Title", content="Some content")
    post2 = create_post(session, author=user_instance, title="Title", content="Some content")
    assert get_all_posts(session) == [post1, post2]
