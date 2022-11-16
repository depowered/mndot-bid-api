import pytest
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm import sessionmaker

from mndot_bid_api.db import models
from mndot_bid_api.db.interface import DBModelInterface
from mndot_bid_api.exceptions import RecordNotFoundError
from tests.data import sample_record_dicts


def test_read_one_by_kwargs_bidders(configured_sessionmaker: sessionmaker):
    model = models.Bidder
    expected_record_dict = sample_record_dicts.sample_bidders[0]
    interface = DBModelInterface(model, configured_sessionmaker)

    # All kwargs
    record_dict = interface.read_one_by_kwargs(**expected_record_dict)
    assert record_dict == expected_record_dict

    # One kwarg
    record_dict = interface.read_one_by_kwargs(name="engineer")
    assert record_dict == expected_record_dict

    # No matches
    with pytest.raises(RecordNotFoundError):
        interface.read_one_by_kwargs(name="no match")

    # Invalid kwarg
    with pytest.raises(InvalidRequestError):
        interface.read_one_by_kwargs(invalid_key=100)


def test_read_one_by_kwargs_contracts(configured_sessionmaker: sessionmaker):
    model = models.Contract
    expected_record_dict = sample_record_dicts.sample_contracts[0]
    interface = DBModelInterface(model, configured_sessionmaker)

    # All kwargs
    record_dict = interface.read_one_by_kwargs(**expected_record_dict)
    assert record_dict == expected_record_dict

    # One kwarg
    record_dict = interface.read_one_by_kwargs(sp_number="5625-20")
    assert record_dict == expected_record_dict

    # No matches
    with pytest.raises(RecordNotFoundError):
        interface.read_one_by_kwargs(county="no match")

    # Invalid kwarg
    with pytest.raises(InvalidRequestError):
        interface.read_one_by_kwargs(invalid_key=100)


def test_read_one_by_kwargs_items(configured_sessionmaker: sessionmaker):
    model = models.Item
    expected_record_dict = sample_record_dicts.sample_items[0]
    interface = DBModelInterface(model, configured_sessionmaker)

    # All kwargs
    record_dict = interface.read_one_by_kwargs(**expected_record_dict)
    assert record_dict == expected_record_dict

    # One kwarg
    record_dict = interface.read_one_by_kwargs(unit="LUMP SUM")
    assert record_dict == expected_record_dict

    # No matches
    with pytest.raises(RecordNotFoundError):
        interface.read_one_by_kwargs(item_code="no match")

    # Invalid kwarg
    with pytest.raises(InvalidRequestError):
        interface.read_one_by_kwargs(invalid_key=100)


def test_read_one_by_kwargs_bids(configured_sessionmaker: sessionmaker):
    model = models.Bid
    expected_record_dict = sample_record_dicts.sample_bids[0]
    interface = DBModelInterface(model, configured_sessionmaker)

    # All kwargs
    record_dict = interface.read_one_by_kwargs(**expected_record_dict)
    assert record_dict == expected_record_dict

    # One kwarg
    record_dict = interface.read_one_by_kwargs(unit_price=580_000)
    assert record_dict == expected_record_dict

    # No matches
    with pytest.raises(RecordNotFoundError):
        interface.read_one_by_kwargs(contract_id=-7)

    # Invalid kwarg
    with pytest.raises(InvalidRequestError):
        interface.read_one_by_kwargs(invalid_key=100)


def test_read_one_by_kwargs_invalid_bids(configured_sessionmaker: sessionmaker):
    model = models.InvalidBid
    expected_record_dict = sample_record_dicts.sample_invalid_bids[0]
    interface = DBModelInterface(model, configured_sessionmaker)

    # All kwargs
    record_dict = interface.read_one_by_kwargs(**expected_record_dict)
    assert record_dict == expected_record_dict

    # One kwarg
    record_dict = interface.read_one_by_kwargs(item_long_description="INSTALL SIGN")
    assert record_dict == expected_record_dict

    # No matches
    with pytest.raises(RecordNotFoundError):
        interface.read_one_by_kwargs(contract_id=-7)

    # Invalid kwarg
    with pytest.raises(InvalidRequestError):
        interface.read_one_by_kwargs(invalid_key=100)
