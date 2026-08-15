from sqlmodel import create_engine, Session, SQLModel
from ..core.config import settings
from typing import Generator

engine = create_engine(settings.database_url, echo=False)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session
