from mndot_bid_api.db import models
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DBSession = sessionmaker()


def init_sqlite_db(url: str) -> None:
    """Intitialize a sqlite database, creating all tables if they do not exist."""
    engine = create_engine(url, connect_args={"check_same_thread": False})
    DBSession.configure(bind=engine, autocommit=False, autoflush=False)
    models.Base.metadata.create_all(bind=engine)
