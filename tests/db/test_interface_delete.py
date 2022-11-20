import pytest
from sqlalchemy.orm import sessionmaker

from mndot_bid_api.db import models
from mndot_bid_api.db.interface import DBModelInterface
from mndot_bid_api.exceptions import RecordNotFoundError


def generic_delete_record_test(record_id: int, interface: DBModelInterface) -> None:
    record_dict = interface.read_by_id(id=record_id)
    record_dicts_before_delete = interface.read_all()
    assert record_dict in record_dicts_before_delete

    interface.delete(id=record_id)

    record_dicts_after_delete = interface.read_all()
    assert record_dict not in record_dicts_after_delete
    assert len(record_dicts_before_delete) - 1 == len(record_dicts_after_delete)

    with pytest.raises(RecordNotFoundError):
        interface.delete(id=record_id)


def test_delete_bidders(configured_sessionmaker: sessionmaker):
    model = models.Bidder
    interface = DBModelInterface(model, configured_sessionmaker)
    record_id = 207897

    generic_delete_record_test(record_id, interface)


def test_delete_contracts(configured_sessionmaker: sessionmaker):
    model = models.Contract
    interface = DBModelInterface(model, configured_sessionmaker)
    record_id = 220005

    generic_delete_record_test(record_id, interface)


def test_delete_items(configured_sessionmaker: sessionmaker):
    model = models.Item
    interface = DBModelInterface(model, configured_sessionmaker)
    record_id = 2

    generic_delete_record_test(record_id, interface)


def test_delete_bids(configured_sessionmaker: sessionmaker):
    model = models.Bid
    interface = DBModelInterface(model, configured_sessionmaker)
    record_id = 2

    generic_delete_record_test(record_id, interface)


def test_delete_invalid_bids(configured_sessionmaker: sessionmaker):
    model = models.Bid
    interface = DBModelInterface(model, configured_sessionmaker)
    record_id = 2

    generic_delete_record_test(record_id, interface)
