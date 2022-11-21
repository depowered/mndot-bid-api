"""
Adapted from:
    https://stackoverflow.com/questions/58660378/how-use-pytest-to-unit-test-sqlalchemy-orm-classes
    https://gist.github.com/kissgyorgy/e2365f25a213de44b9a2
"""
import fastapi
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from mndot_bid_api import db, routers
from mndot_bid_api.db import interface, models
from tests.data import sample_db_records


@pytest.fixture(scope="session")
def engine():
    return create_engine(
        "sqlite:///tests/data/test-api.db", connect_args={"check_same_thread": False}
    )


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


@pytest.fixture(scope="function")
def get_bidder_interface_override(configured_sessionmaker: sessionmaker):
    return lambda: interface.DBModelInterface(models.Bidder, configured_sessionmaker)


@pytest.fixture(scope="function")
def get_contract_interface_override(configured_sessionmaker: sessionmaker):
    return lambda: interface.DBModelInterface(models.Contract, configured_sessionmaker)


@pytest.fixture(scope="function")
def get_bid_interface_override(configured_sessionmaker: sessionmaker):
    return lambda: interface.DBModelInterface(models.Bid, configured_sessionmaker)


@pytest.fixture(scope="function")
def get_invalid_bid_interface_override(configured_sessionmaker: sessionmaker):
    return lambda: interface.DBModelInterface(
        models.InvalidBid, configured_sessionmaker
    )


@pytest.fixture(scope="function")
def get_item_interface_override(configured_sessionmaker: sessionmaker):
    return lambda: interface.DBModelInterface(models.Item, configured_sessionmaker)


@pytest.fixture(scope="function")  # Or function?
def test_client(
    get_bidder_interface_override,
    get_contract_interface_override,
    get_bid_interface_override,
    get_invalid_bid_interface_override,
    get_item_interface_override,
) -> TestClient:
    # Initilize test_app instance
    test_app = fastapi.FastAPI()

    # Override get_<model>_interface functions
    test_app.dependency_overrides[
        db.get_bidder_interface
    ] = get_bidder_interface_override

    test_app.dependency_overrides[
        db.get_contract_interface
    ] = get_contract_interface_override

    test_app.dependency_overrides[db.get_bid_interface] = get_bid_interface_override

    test_app.dependency_overrides[
        db.get_invalid_bid_interface
    ] = get_invalid_bid_interface_override

    test_app.dependency_overrides[db.get_item_interface] = get_item_interface_override

    # Duplicate root path from main
    @test_app.get("/", include_in_schema=False)
    def read_root():
        return {"server status": "Running"}

    # Add all routes
    test_app.include_router(routers.bidder_router)
    test_app.include_router(routers.contract_router)
    test_app.include_router(routers.bid_router)
    test_app.include_router(routers.invalid_bid_router)
    test_app.include_router(routers.item_router)
    test_app.include_router(routers.etl_router)

    # Itialize and return the test client
    test_client = TestClient(test_app)
    return test_client


@pytest.fixture(scope="function")
def abstract_csv_file():
    with open("./tests/data/220005.csv", "rb") as f:
        yield f


@pytest.fixture(scope="function")
def abstract_csv_content(abstract_csv_file):
    return abstract_csv_file.read().decode()


@pytest.fixture(scope="function")
def item_list_csv_file():
    with open("./tests/data/item_list_2016.csv", "rb") as f:
        yield f


@pytest.fixture(scope="function")
def item_list_csv_content(item_list_csv_file):
    return item_list_csv_file.read().decode()
