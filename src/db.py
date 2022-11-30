from datetime import datetime
from sqlalchemy import create_engine, Column, Table, Integer, String, Boolean, Text, DateTime, func
from sqlalchemy.orm import declarative_base, Session as SessionType, sessionmaker, scoped_session

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


def create_user(session: SessionType, name, password):
    user = User(name=name, password=password)
    is_user_exists = session.query(User).filter_by(name=name).first()
    if is_user_exists:
        raise InvalidUserName("User with the same name already exists")
    session.add(user)
    session.commit()
    return user


def main():
    Base.metadata.drop_all()
    Base.metadata.create_all()

    session: SessionType = Session()
    create_user(session, "Ivan")
    session.close()


if __name__ == "__main__":
    main()
