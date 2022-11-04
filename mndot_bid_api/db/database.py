from collections.abc import Generator

from mndot_bid_api.db import models
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

# engine: Engine | None = None
DBSession = sessionmaker()


def init_sqlite_db(url: str) -> None:
    engine = create_engine(url, connect_args={"check_same_thread": False})
    DBSession.configure(bind=engine, autocommit=False, autoflush=False)
    models.Base.metadata.create_all(bind=engine)


def get_db_session() -> Generator[Session, None, None]:
    db: Session = DBSession()
    try:
        yield db
    finally:
        db.close()


class SessionContextManager:
    def __init__(self):
        self.db = DBSession()

    def __enter__(self):
        return self.db

    def __exit__(self, exc_type, exc_value, traceback):
        self.db.close()
