from sqlmodel import create_engine, SQLModel, Session

from src.core.settings.config import settings


engine = create_engine(url=settings.POSTGRES_URL, echo=True)

def init_db():
    SQLModel.metadata.create_all(bind=engine)


def get_session():
    with Session(engine) as session:
        yield session