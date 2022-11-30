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

    posts = relationship("Post", back_populates="author")
    comments = relationship("Comment", back_populates="author")

    def __repr__(self):
        return f"User(id={self.id!r}, name={self.name!r}, created_at={self.created_at!r})"


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String(96), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow(), server_default=func.now())

    author = relationship("User", back_populates="posts")
    comments = relationship("Comment", back_populates="post")

    def __repr__(self):
        return f"Post(id={self.id!r}, title={self.title!r}, created_at:{self.created_at!r})"


class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    post_id = Column(Integer, ForeignKey("posts.id"), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow(), server_default=func.now())

    author = relationship("User", back_populates="comments")
    post = relationship("Post", back_populates="comments")

    def __repr__(self):
        return f"Comment(id={self.id!r}, author_id={self.author_id!r}, content={self.content!r}, created_at:{self.created_at!r})"


def add_record(session: SessionType, record):
    session.add(record)
    session.commit()


def create_user(session: SessionType, name, password):
    user = User(name=name, password=password)
    is_user_exists = session.query(User).filter_by(name=name).first()
    if is_user_exists:
        raise InvalidUserName("User with the same name already exists")
    add_record(session, user)
    return user


def create_post(session: SessionType, author: User, title, content):
    post = Post(author=author, title=title, content=content)
    add_record(session, post)
    return post


def create_comment(session: SessionType, post, author, content):
    comment = Comment(author=author, post=post, content=content)
    add_record(session, comment)
    return comment


def get_user_posts(session: SessionType, user: User):
    return session.query(Comment).filter_by(author=user).all()


def main():
    Base.metadata.drop_all()
    Base.metadata.create_all()

    session: SessionType = Session()
    user = create_user(session, "Ivan", "1234")
    post = create_post(session, user, "Title", "Lorem ipsum")
    session.close()


if __name__ == "__main__":
    main()
