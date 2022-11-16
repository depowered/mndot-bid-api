from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker

from mndot_bid_api.db import models


def test_add_bidder_record_rollback(configured_sessionmaker: sessionmaker):
    with configured_sessionmaker() as dbsession:
        starting_record_count = len(dbsession.query(models.Bidder).all())
        assert starting_record_count == 6

        record = models.Bidder(id=-100, name="Record to rollback")
        dbsession.add(record)

        ending_record_count = len(dbsession.query(models.Bidder).all())
        assert ending_record_count == 7


def test_bidder_record_count_after_rollback(configured_sessionmaker: sessionmaker):
    with configured_sessionmaker() as dbsession:
        starting_record_count = len(dbsession.query(models.Bidder).all())
        assert starting_record_count == 6


def test_get_bidder_interface_override(get_bidder_interface_override):
    interface = get_bidder_interface_override()
    assert isinstance(interface.model(), models.Bidder)


def test_get_contract_interface_override(get_contract_interface_override):
    interface = get_contract_interface_override()
    assert isinstance(interface.model(), models.Contract)


def test_get_bid_interface_override(get_bid_interface_override):
    interface = get_bid_interface_override()
    assert isinstance(interface.model(), models.Bid)


def test_get_invalid_bid_interface_override(get_invalid_bid_interface_override):
    interface = get_invalid_bid_interface_override()
    assert isinstance(interface.model(), models.InvalidBid)


def test_get_item_interface_override(get_item_interface_override):
    interface = get_item_interface_override()
    assert isinstance(interface.model(), models.Item)


def test_test_app_running(test_client: TestClient):
    response = test_client.get("/")
    assert response.status_code == 200
    assert response.json() == {"server status": "Running"}
