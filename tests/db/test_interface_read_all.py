from sqlalchemy.orm import sessionmaker

from mndot_bid_api.db import models
from mndot_bid_api.db.interface import DBModelInterface, RecordDict
from tests.data import sample_record_dicts


def generic_read_all_test(
    configured_sessionmaker: sessionmaker,
    model: models.Base,
    expected_result: list[RecordDict],
) -> None:
    interface = DBModelInterface(model, configured_sessionmaker)
    record_dicts = interface.read_all()
    assert len(record_dicts) == len(expected_result)

    for record_dict in record_dicts:
        assert record_dict in expected_result


def test_read_all_bidders(configured_sessionmaker: sessionmaker):
    generic_read_all_test(
        configured_sessionmaker, models.Bidder, sample_record_dicts.sample_bidders
    )


def test_read_all_contracts(configured_sessionmaker: sessionmaker):
    generic_read_all_test(
        configured_sessionmaker, models.Contract, sample_record_dicts.sample_contracts
    )


def test_read_all_items(configured_sessionmaker: sessionmaker):
    generic_read_all_test(
        configured_sessionmaker, models.Item, sample_record_dicts.sample_items
    )


def test_read_all_bids(configured_sessionmaker: sessionmaker):
    generic_read_all_test(
        configured_sessionmaker, models.Bid, sample_record_dicts.sample_bids
    )


def test_read_all_invalid_bids(configured_sessionmaker: sessionmaker):
    generic_read_all_test(
        configured_sessionmaker,
        models.InvalidBid,
        sample_record_dicts.sample_invalid_bids,
    )


def test_empty_result(configured_sessionmaker: sessionmaker):
    interface = DBModelInterface(models.Contract, configured_sessionmaker)
    # Delete the one record in the contract table
    interface.delete(id=220005)
    # Read all should return an empty list now
    record_dicts = interface.read_all()
    assert not record_dicts
