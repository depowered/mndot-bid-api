import pytest
from sqlalchemy.orm import sessionmaker

from mndot_bid_api.db import models
from mndot_bid_api.db.interface import DBModelInterface
from mndot_bid_api.exceptions import RecordNotFoundException


def test_update_bidders(configured_sessionmaker: sessionmaker):
    model = models.Bidder
    interface = DBModelInterface(model, configured_sessionmaker)
    record_id = 207897

    record_dict_before_update = interface.read_by_id(record_id)
    assert record_dict_before_update["name"] == "Central Specialties, Inc."

    update_data_dict = {"name": "Name has changed"}
    expected_record_dict = record_dict_before_update.copy()
    expected_record_dict.update(update_data_dict)

    record_dict = interface.update(id=record_id, data=update_data_dict)
    assert record_dict == expected_record_dict

    with pytest.raises(RecordNotFoundException):
        interface.update(id=-7, data=update_data_dict)


def test_update_contracts(configured_sessionmaker: sessionmaker):
    model = models.Contract
    interface = DBModelInterface(model, configured_sessionmaker)
    record_id = 220005

    record_dict_before_update = interface.read_by_id(record_id)
    assert record_dict_before_update["sp_number"] == "5625-20"
    assert record_dict_before_update["district"] == "Detroit Lakes"

    update_data_dict = {"sp_number": "1234-56", "district": "Metro"}
    expected_record_dict = record_dict_before_update.copy()
    expected_record_dict.update(update_data_dict)

    record_dict = interface.update(id=record_id, data=update_data_dict)
    assert record_dict == expected_record_dict

    with pytest.raises(RecordNotFoundException):
        interface.update(id=-7, data=update_data_dict)


def test_update_items(configured_sessionmaker: sessionmaker):
    model = models.Item
    interface = DBModelInterface(model, configured_sessionmaker)
    record_id = 2

    record_dict_before_update = interface.read_by_id(record_id)
    assert record_dict_before_update["in_spec_2022"] is False
    assert record_dict_before_update["short_description"] == "EXCAVATION - COMMON"

    update_data_dict = {"in_spec_2022": True, "short_description": "COMMON EX"}
    expected_record_dict = record_dict_before_update.copy()
    expected_record_dict.update(update_data_dict)

    record_dict = interface.update(id=record_id, data=update_data_dict)
    assert record_dict == expected_record_dict

    with pytest.raises(RecordNotFoundException):
        interface.update(id=-7, data=update_data_dict)


def test_update_bids(configured_sessionmaker: sessionmaker):
    model = models.Bid
    interface = DBModelInterface(model, configured_sessionmaker)
    record_id = 7

    record_dict_before_update = interface.read_by_id(record_id)
    assert record_dict_before_update["quantity"] == 3725
    assert record_dict_before_update["unit_price"] == 15_42

    update_data_dict = {"quantity": 20_000, "unit_price": 8_00}
    expected_record_dict = record_dict_before_update.copy()
    expected_record_dict.update(update_data_dict)

    record_dict = interface.update(id=record_id, data=update_data_dict)
    assert record_dict == expected_record_dict

    with pytest.raises(RecordNotFoundException):
        interface.update(id=-7, data=update_data_dict)


def test_update_invalid_bids(configured_sessionmaker: sessionmaker):
    model = models.InvalidBid
    interface = DBModelInterface(model, configured_sessionmaker)
    record_id = 2

    record_dict_before_update = interface.read_by_id(record_id)
    assert record_dict_before_update["quantity"] == 28
    assert record_dict_before_update["bid_type"] == "winning"

    update_data_dict = {"quantity": 32, "bid_type": "losing"}
    expected_record_dict = record_dict_before_update.copy()
    expected_record_dict.update(update_data_dict)

    record_dict = interface.update(id=record_id, data=update_data_dict)
    assert record_dict == expected_record_dict

    with pytest.raises(RecordNotFoundException):
        interface.update(id=-7, data=update_data_dict)
