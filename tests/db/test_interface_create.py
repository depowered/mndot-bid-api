from datetime import date

import pytest
from sqlalchemy.orm import sessionmaker

from mndot_bid_api.db import models
from mndot_bid_api.db.interface import DBModelInterface
from mndot_bid_api.exceptions import RecordAlreadyExistsException


def test_create_bidders(configured_sessionmaker: sessionmaker):
    model = models.Bidder
    interface = DBModelInterface(model, configured_sessionmaker)

    record_dicts_before_create = interface.read_all()

    create_data_dict = {"id": 9999, "name": "My Favorite Contractor"}
    expected_record_dict = create_data_dict.copy()

    record_dict = interface.create(data=create_data_dict)
    assert record_dict == expected_record_dict

    record_dicts_after_create = interface.read_all()
    assert len(record_dicts_before_create) == len(record_dicts_after_create) - 1
    assert record_dict in record_dicts_after_create

    with pytest.raises(RecordAlreadyExistsException) as exc:
        interface.create(data=create_data_dict)
    assert exc.value.args[0]["id"] == 9999


def test_create_contracts(configured_sessionmaker: sessionmaker):
    model = models.Contract
    interface = DBModelInterface(model, configured_sessionmaker)

    record_dicts_before_create = interface.read_all()

    create_data_dict = {
        "id": 1001,
        "letting_date": date(1999, 12, 31),
        "sp_number": "1234-56",
        "district": "Metro",
        "county": "HENNEPIN",
        "description": "Fixing some pavement",
        "winning_bidder_id": 1111,
    }
    expected_record_dict = create_data_dict.copy()

    record_dict = interface.create(data=create_data_dict)
    assert record_dict == expected_record_dict

    record_dicts_after_create = interface.read_all()
    assert len(record_dicts_before_create) == len(record_dicts_after_create) - 1
    assert record_dict in record_dicts_after_create

    with pytest.raises(RecordAlreadyExistsException) as exc:
        interface.create(data=create_data_dict)
    assert exc.value.args[0]["id"] == 1001


def test_create_items(configured_sessionmaker: sessionmaker):
    model = models.Item
    interface = DBModelInterface(model, configured_sessionmaker)

    record_dicts_before_create = interface.read_all()

    create_data_dict = {
        "spec_code": "1111",
        "unit_code": "222",
        "item_code": "33333",
        "short_description": "desc",
        "long_description": "description",
        "unit": "LIN FT",
        "unit_abbreviation": "LF",
        "in_spec_2016": True,
    }

    expected_record_dict = create_data_dict.copy()
    expected_record_dict.update(
        id=3,  # autoincremented id
        # the unspecified in_spec_#### should default to False
        in_spec_2018=False,
        in_spec_2020=False,
        in_spec_2022=False,
    )

    record_dict = interface.create(data=create_data_dict)
    assert record_dict == expected_record_dict

    record_dicts_after_create = interface.read_all()
    assert len(record_dicts_before_create) == len(record_dicts_after_create) - 1
    assert record_dict in record_dicts_after_create

    with pytest.raises(RecordAlreadyExistsException) as exc:
        interface.create(data=create_data_dict)
    assert exc.value.args[0]["id"] == 3


def test_create_bids(configured_sessionmaker: sessionmaker):
    model = models.Bid
    interface = DBModelInterface(model, configured_sessionmaker)

    record_dicts_before_create = interface.read_all()

    create_data_dict = {
        "contract_id": 123456,
        "bidder_id": 9876,
        "item_id": 2,
        "quantity": 20_000.01,
        "unit_price": 5_00,
        "bid_type": "losing",
    }

    expected_record_dict = create_data_dict.copy()
    expected_record_dict.update(id=13)  # autoincremented id

    record_dict = interface.create(data=create_data_dict)
    assert record_dict == expected_record_dict

    record_dicts_after_create = interface.read_all()
    assert len(record_dicts_before_create) == len(record_dicts_after_create) - 1
    assert record_dict in record_dicts_after_create

    with pytest.raises(RecordAlreadyExistsException) as exc:
        interface.create(data=create_data_dict)
    assert exc.value.args[0]["id"] == 13


def test_create_invalid_bids(configured_sessionmaker: sessionmaker):
    model = models.InvalidBid
    interface = DBModelInterface(model, configured_sessionmaker)

    record_dicts_before_create = interface.read_all()

    create_data_dict = {
        "contract_id": 123456,
        "bidder_id": 9876,
        "item_spec_code": "1111",
        "item_unit_code": "222",
        "item_item_code": "33333",
        "item_long_description": "description",
        "item_unit_abbreviation": "LF",
        "quantity": 20_000.01,
        "unit_price": 5_00,
        "bid_type": "losing",
    }

    expected_record_dict = create_data_dict.copy()
    expected_record_dict.update(id=7)  # autoincremented id

    record_dict = interface.create(data=create_data_dict)
    assert record_dict == expected_record_dict

    record_dicts_after_create = interface.read_all()
    assert len(record_dicts_before_create) == len(record_dicts_after_create) - 1
    assert record_dict in record_dicts_after_create

    with pytest.raises(RecordAlreadyExistsException) as exc:
        interface.create(data=create_data_dict)
    assert exc.value.args[0]["id"] == 7
