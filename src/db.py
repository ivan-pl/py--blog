from datetime import datetime
from sqlalchemy import create_engine, Column, Table, Integer, String, Boolean, Text, DateTime, func
from sqlalchemy.orm import declarative_base, Session as SessionType, sessionmaker, scoped_session

DB_URL = "postgresql+psycopg2://user:userpass@localhost/blog"
DB_ECHO = False

engine = create_engine(DB_URL)
Base = declarative_base(bind=engine)
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String(32), unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow(), server_default=func.now())

    def __repr__(self):
        return f"User(id={self.id!r}, name={self.name!r}, created_at={self.created_at!r})"


def create_user(session: SessionType, name):
    user = User(name=name)
    print("user", user)
    session.add(user)
    print("user added", user)
    session.commit()
    print("user saved", user)
    return user


def main():
    Base.metadata.drop_all()
    Base.metadata.create_all()

    session: SessionType = Session()
    create_user(session, "Ivan")
    session.close()


if __name__ == "__main__":
    main()
