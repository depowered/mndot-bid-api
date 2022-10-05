from mndot_bid_api.db import models
from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import Session, sessionmaker

engine: Engine = None
DBSession = sessionmaker()


def init_sqlite_db(url: str) -> None:
    engine = create_engine(url, connect_args={"check_same_thread": False})
    DBSession.configure(
        bind=engine, autocommit=False, autoflush=False
    )  # = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    models.Base.metadata.create_all(bind=engine)


def get_db_session() -> Session:
    try:
        db: Session = DBSession()
        yield db
    finally:
        db.close()
