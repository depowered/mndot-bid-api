import pytest
from sqlalchemy.orm import sessionmaker

from mndot_bid_api.db import models
from mndot_bid_api.db.interface import DBModelInterface, RecordDict
from mndot_bid_api.exceptions import RecordNotFoundException
from tests.data import sample_record_dicts


def generic_read_by_id_test(
    configured_sessionmaker: sessionmaker,
    model: models.Base,
    expected_record_dicts: list[RecordDict],
) -> None:
    interface = DBModelInterface(model, configured_sessionmaker)
    for expected_record_dict in expected_record_dicts:
        record_dict = interface.read_by_id(expected_record_dict["id"])
        assert record_dict == expected_record_dict


def generic_read_by_id_raises_record_not_found_test(
    configured_sessionmaker: sessionmaker, model: models.Base
) -> None:
    interface = DBModelInterface(model, configured_sessionmaker)
    with pytest.raises(RecordNotFoundException):
        interface.read_by_id(-7)


def test_read_by_id_bidders(configured_sessionmaker: sessionmaker):
    model = models.Bidder
    expected_record_dicts = sample_record_dicts.sample_bidders
    generic_read_by_id_test(configured_sessionmaker, model, expected_record_dicts)
    generic_read_by_id_raises_record_not_found_test(configured_sessionmaker, model)


def test_read_by_id_contracts(configured_sessionmaker: sessionmaker):
    model = models.Contract
    expected_record_dicts = sample_record_dicts.sample_contracts
    generic_read_by_id_test(configured_sessionmaker, model, expected_record_dicts)
    generic_read_by_id_raises_record_not_found_test(configured_sessionmaker, model)


def test_read_by_id_items(configured_sessionmaker: sessionmaker):
    model = models.Item
    expected_record_dicts = sample_record_dicts.sample_items
    generic_read_by_id_test(configured_sessionmaker, model, expected_record_dicts)
    generic_read_by_id_raises_record_not_found_test(configured_sessionmaker, model)


def test_read_by_id_bids(configured_sessionmaker: sessionmaker):
    model = models.Bid
    expected_record_dicts = sample_record_dicts.sample_bids
    generic_read_by_id_test(configured_sessionmaker, model, expected_record_dicts)
    generic_read_by_id_raises_record_not_found_test(configured_sessionmaker, model)


def test_read_by_id_invalid_bids(configured_sessionmaker: sessionmaker):
    model = models.InvalidBid
    expected_record_dicts = sample_record_dicts.sample_invalid_bids
    generic_read_by_id_test(configured_sessionmaker, model, expected_record_dicts)
    generic_read_by_id_raises_record_not_found_test(configured_sessionmaker, model)
