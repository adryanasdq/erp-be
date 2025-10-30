from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session as SessionType
from sqlmodel import SQLModel

from src.core.settings.config import settings

# This file is responsible for creating the database engine and session
# and initializing the database.
engine = create_engine(url=settings.POSTGRES_URL, echo=True)

def init_db():
    SQLModel.metadata.create_all(bind=engine)


def get_session():
    session = sessionmaker(
        bind=engine,
        class_=SessionType,
        expire_on_commit=False,
    )

    with session() as session:
        yield session