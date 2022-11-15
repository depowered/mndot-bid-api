"""
Adapted from:
    https://stackoverflow.com/questions/58660378/how-use-pytest-to-unit-test-sqlalchemy-orm-classes
    https://gist.github.com/kissgyorgy/e2365f25a213de44b9a2
"""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from mndot_bid_api.db import models
from tests.data import sample_db_records


@pytest.fixture(scope="session")
def engine():
    return create_engine("sqlite:///tests/data/test-api.db")


@pytest.fixture(scope="session")
def tables(engine):
    # If the previous run failed to return the fixture, such as in a stopped
    # debugging session, data may still exist in the database. Drop tables
    # before continuing to avoid conflicts in the load sample data step.
    models.Base.metadata.drop_all(engine)

    # Create tables
    models.Base.metadata.create_all(engine)

    # Load sample data
    with Session(bind=engine) as db:
        db.add_all(sample_db_records.bidders)
        db.add_all(sample_db_records.contracts)
        db.add_all(sample_db_records.items)
        db.add_all(sample_db_records.bids)
        db.add_all(sample_db_records.invalid_bids)
        db.commit()

    yield

    # Drop tables
    models.Base.metadata.drop_all(engine)


@pytest.fixture(scope="function")
def configured_sessionmaker(engine, tables):
    """Returns an sqlalchemy session, and after the test tears down everything properly."""
    connection = engine.connect()
    # begin the nested transaction
    transaction = connection.begin()
    # use the connection with the already started transaction
    conf_sessionmaker = sessionmaker(bind=connection)

    yield conf_sessionmaker

    # roll back the broader transaction
    transaction.rollback()
    # put back the connection to the connection pool
    connection.close()
