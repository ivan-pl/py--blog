from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, func, ForeignKey
from sqlalchemy.orm import declarative_base, Session as SessionType, sessionmaker, scoped_session, relationship

DB_URL = "postgresql+psycopg2://user:userpass@localhost/blog"
DB_ECHO = False

engine = create_engine(DB_URL)
Base = declarative_base(bind=engine)
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)


class InvalidUserName(Exception):
    def __init__(self, message):
        super().__init__(message)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String(32), unique=True, nullable=False)
    password = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow(), server_default=func.now())

    def __repr__(self):
        return f"User(id={self.id!r}, name={self.name!r}, created_at={self.created_at!r})"


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String(96), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow(), server_default=func.now())

    def __repr__(self):
        return f"Post(id={self.id!r}, title={self.title!r}, created_at:{self.created_at!r}"


def create_user(session: SessionType, name, password):
    user = User(name=name, password=password)
    is_user_exists = session.query(User).filter_by(name=name).first()
    if is_user_exists:
        raise InvalidUserName("User with the same name already exists")
    session.add(user)
    session.commit()
    return user


def create_post(session: SessionType, author: User, title, content):
    post = Post(author_id=author.id, title=title, content=content)
    session.add(post)
    session.commit()
    return post


def main():
    Base.metadata.drop_all()
    Base.metadata.create_all()

    session: SessionType = Session()
    user = create_user(session, "Ivan", "1234")
    post = create_post(session, user, "Title", "Lorem ipsum")
    session.close()


if __name__ == "__main__":
    main()
