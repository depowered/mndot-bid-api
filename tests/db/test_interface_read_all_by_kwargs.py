import pytest
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm import sessionmaker

from mndot_bid_api.db import models
from mndot_bid_api.db.interface import DBModelInterface
from mndot_bid_api.exceptions import RecordNotFoundError
from tests.data import sample_record_dicts


def test_read_all_by_kwargs_bidders(configured_sessionmaker: sessionmaker):
    model = models.Bidder
    expected_record_dicts = sample_record_dicts.sample_bidders
    interface = DBModelInterface(model, configured_sessionmaker)

    # All kwargs
    record_dicts = interface.read_all_by_kwargs(id=0, name="engineer")
    assert isinstance(record_dicts, list)
    assert len(record_dicts) == 1
    assert record_dicts[0] == expected_record_dicts[0]

    # One kwarg
    record_dicts = interface.read_all_by_kwargs(name="Central Specialties, Inc.")
    assert len(record_dicts) == 1
    assert record_dicts[0] == expected_record_dicts[1]

    # No matches
    with pytest.raises(RecordNotFoundError):
        interface.read_all_by_kwargs(name="no match")

    # Invalid kwarg
    with pytest.raises(InvalidRequestError):
        interface.read_all_by_kwargs(invalid_key=100)

    # Test positive limit; expect one record
    record_dicts = interface.read_all_by_kwargs(limit=1, name="Central Specialties, Inc.")
    assert len(record_dicts) == 1

    # Test negative limit; expect no records
    record_dicts = interface.read_all_by_kwargs(limit=-1, name="Central Specialties, Inc.")
    assert len(record_dicts) == 0


def test_read_all_by_kwargs_contracts(configured_sessionmaker: sessionmaker):
    model = models.Contract
    expected_record_dicts = sample_record_dicts.sample_contracts
    interface = DBModelInterface(model, configured_sessionmaker)

    # All kwargs
    record_dicts = interface.read_all_by_kwargs(**expected_record_dicts[0])
    assert isinstance(record_dicts, list)
    assert len(record_dicts) == 1
    assert record_dicts == expected_record_dicts

    # One kwarg
    record_dicts = interface.read_all_by_kwargs(sp_number="5625-20")
    assert record_dicts == expected_record_dicts

    # No matches
    with pytest.raises(RecordNotFoundError):
        interface.read_all_by_kwargs(county="no match")

    # Invalid kwarg
    with pytest.raises(InvalidRequestError):
        interface.read_all_by_kwargs(invalid_key=100)

    # Test positive limit; expect one record
    record_dicts = interface.read_all_by_kwargs(limit=1, sp_number="5625-20")
    assert len(record_dicts) == 1

    # Test negative limit; expect no records
    record_dicts = interface.read_all_by_kwargs(limit=-1, sp_number="5625-20")
    assert len(record_dicts) == 0


def test_read_all_by_kwargs_items(configured_sessionmaker: sessionmaker):
    model = models.Item
    expected_record_dicts = sample_record_dicts.sample_items
    interface = DBModelInterface(model, configured_sessionmaker)

    # All kwargs
    record_dicts = interface.read_all_by_kwargs(**expected_record_dicts[0])
    assert isinstance(record_dicts, list)
    assert len(record_dicts) == 1
    assert record_dicts[0] == expected_record_dicts[0]

    # One kwarg
    record_dicts = interface.read_all_by_kwargs(in_spec_2020=True)
    assert len(record_dicts) == 2
    for record_dict in record_dicts:
        assert record_dict in expected_record_dicts

    # No matches
    with pytest.raises(RecordNotFoundError):
        interface.read_all_by_kwargs(item_code="no match")

    # Invalid kwarg
    with pytest.raises(InvalidRequestError):
        interface.read_all_by_kwargs(invalid_key=100)

    # Test positive limit; expect one record
    record_dicts = interface.read_all_by_kwargs(limit=1, in_spec_2020=True)
    assert len(record_dicts) == 1

    # Test negative limit; expect no records
    record_dicts = interface.read_all_by_kwargs(limit=-1, in_spec_2020=True)
    assert len(record_dicts) == 0


def test_read_all_by_kwargs_bids(configured_sessionmaker: sessionmaker):
    model = models.Bid
    expected_record_dicts = sample_record_dicts.sample_bids
    interface = DBModelInterface(model, configured_sessionmaker)

    # All kwargs
    record_dicts = interface.read_all_by_kwargs(**expected_record_dicts[1])
    assert isinstance(record_dicts, list)
    assert len(record_dicts) == 1
    assert record_dicts[0] == expected_record_dicts[1]

    # One kwarg
    record_dicts = interface.read_all_by_kwargs(bid_type="losing")
    assert len(record_dicts) == 8
    assert expected_record_dicts[2] in record_dicts

    # No matches
    with pytest.raises(RecordNotFoundError):
        interface.read_all_by_kwargs(contract_id=-7)

    # Invalid kwarg
    with pytest.raises(InvalidRequestError):
        interface.read_all_by_kwargs(invalid_key=100)

    # Test positive limit; expect one record
    record_dicts = interface.read_all_by_kwargs(limit=1, bid_type="losing")
    assert len(record_dicts) == 1

    # Test negative limit; expect no records
    record_dicts = interface.read_all_by_kwargs(limit=-1, bid_type="losing")
    assert len(record_dicts) == 0


def test_read_all_by_kwargs_invalid_bids(configured_sessionmaker: sessionmaker):
    model = models.InvalidBid
    expected_record_dicts = sample_record_dicts.sample_invalid_bids
    interface = DBModelInterface(model, configured_sessionmaker)

    # All kwargs
    record_dicts = interface.read_all_by_kwargs(**expected_record_dicts[1])
    assert isinstance(record_dicts, list)
    assert len(record_dicts) == 1
    assert record_dicts[0] == expected_record_dicts[1]

    # One kwarg
    record_dicts = interface.read_all_by_kwargs(bid_type="losing")
    assert len(record_dicts) == 4
    for record_dict in record_dicts:
        assert record_dict in expected_record_dicts[-4:]

    # No matches
    with pytest.raises(RecordNotFoundError):
        interface.read_all_by_kwargs(contract_id=-7)

    # Invalid kwarg
    with pytest.raises(InvalidRequestError):
        interface.read_all_by_kwargs(invalid_key=100)

    # Test positive limit; expect one record
    record_dicts = interface.read_all_by_kwargs(limit=1, bid_type="losing")
    assert len(record_dicts) == 1

    # Test negative limit; expect no records
    record_dicts = interface.read_all_by_kwargs(limit=-1, bid_type="losing")
    assert len(record_dicts) == 0
