from mndot_bid_api.db import models
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DBSession = sessionmaker()


def init_sqlite_db(url: str) -> None:
    engine = create_engine(url, connect_args={"check_same_thread": False})
    DBSession.configure(bind=engine, autocommit=False, autoflush=False)
    models.Base.metadata.create_all(bind=engine)
