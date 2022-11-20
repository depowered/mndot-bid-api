from datetime import date

import fastapi
import pytest
from sqlalchemy.orm import sessionmaker

from mndot_bid_api import operations
from mndot_bid_api.db import models
from mndot_bid_api.db.interface import DBModelInterface
from mndot_bid_api.exceptions import InvalidBidError, RecordAlreadyExistsError
from mndot_bid_api.operations import enums, schema


def test_create_bidders(configured_sessionmaker: sessionmaker):
    model = models.Bidder
    interface = DBModelInterface(model, configured_sessionmaker)
    result_data_schema = schema.BidderResult
    result_schema = schema.Bidder
    operation_function = operations.bidders.create_bidder

    create_data = schema.BidderCreateData(id=9999, name="Worlds newest contractor")

    expected_data_result = result_data_schema(**create_data.dict())
    expected_result = result_schema(data=expected_data_result)

    result = operation_function(create_data, interface)
    assert result.type == expected_result.type
    assert result.data == expected_result.data

    with pytest.raises(fastapi.HTTPException) as exc:
        operation_function(create_data, interface)
    assert exc.value.status_code == 303


def test_create_contracts(configured_sessionmaker: sessionmaker):
    model = models.Contract
    interface = DBModelInterface(model, configured_sessionmaker)
    result_data_schema = schema.ContractResult
    result_schema = schema.Contract
    operation_function = operations.contracts.create_contract

    create_data = schema.ContractCreateData(
        id=1001,
        letting_date=date(1999, 12, 31),
        sp_number="1234-56",
        district=enums.District.METRO,
        county=enums.County.HENNEPIN,
        description="Fixing some pavement",
        winning_bidder_id=1111,
    )

    expected_data_result = result_data_schema(**create_data.dict())
    expected_result = result_schema(data=expected_data_result)

    result = operation_function(create_data, interface)
    assert result.type == expected_result.type
    assert result.data == expected_result.data

    with pytest.raises(fastapi.HTTPException) as exc:
        operation_function(create_data, interface)
    assert exc.value.status_code == 303


def test_create_items(configured_sessionmaker: sessionmaker):
    model = models.Item
    interface = DBModelInterface(model, configured_sessionmaker)
    result_data_schema = schema.ItemResult
    result_schema = schema.Item
    operation_function = operations.items.create_item

    create_data = schema.ItemCreateData(
        spec_code="1111",
        unit_code="222",
        item_code="33333",
        short_description="desc",
        long_description="description",
        unit="LIN FT",
        unit_abbreviation="LF",
        in_spec_2016=True,
    )

    expected_record_dict = create_data.dict()
    expected_record_dict.update(
        id=3,  # autoincremented id
        # the unspecified in_spec_#### should default to False
        in_spec_2018=False,
        in_spec_2020=False,
        in_spec_2022=False,
    )
    expected_data_result = result_data_schema(**expected_record_dict)
    expected_result = result_schema(data=expected_data_result)

    result = operation_function(create_data, interface)
    assert result.type == expected_result.type
    assert result.data == expected_result.data

    with pytest.raises(fastapi.HTTPException) as exc:
        operation_function(create_data, interface)
    assert exc.value.status_code == 303


def test_create_bids(configured_sessionmaker: sessionmaker):
    bid_interface = DBModelInterface(models.Bid, configured_sessionmaker)
    item_interface = DBModelInterface(models.Item, configured_sessionmaker)
    result_data_schema = schema.BidResult
    result_schema = schema.Bid
    operation_function = operations.bids.create_bid

    create_data = schema.BidCreateData(
        contract_id=9999,
        bidder_id=123456,
        item_spec_code="2011",
        item_unit_code="601",
        item_item_code="01000",
        item_long_description="AS BUILT",
        item_unit_abbreviation="LS",
        quantity=20_000.01,
        unit_price=5_00,
        bid_type=enums.BidType.LOSING,
    )

    expected_record_dict = create_data.dict()
    expected_record_dict.update(id=13, item_id=1)
    expected_data_result = result_data_schema(**expected_record_dict)
    expected_result = result_schema(data=expected_data_result)

    result = operation_function(create_data, bid_interface, item_interface)
    assert result.type == expected_result.type
    assert result.data == expected_result.data

    with pytest.raises(fastapi.HTTPException) as exc:
        operation_function(create_data, bid_interface, item_interface)
    assert exc.value.status_code == 303

    create_data.item_spec_code = "9999"
    with pytest.raises(InvalidBidError):
        operation_function(create_data, bid_interface, item_interface)


def test_create_invalid_bids(configured_sessionmaker: sessionmaker):
    model = models.InvalidBid
    interface = DBModelInterface(model, configured_sessionmaker)
    result_data_schema = schema.InvalidBidResult
    result_schema = schema.InvalidBid
    operation_function = operations.invalid_bids.create_invalid_bid

    create_data = schema.BidCreateData(
        contract_id=9999,
        bidder_id=123456,
        item_spec_code="2011",
        item_unit_code="601",
        item_item_code="01000",
        item_long_description="AS BUILT",
        item_unit_abbreviation="LS",
        quantity=20_000.01,
        unit_price=5_00,
        bid_type=enums.BidType.LOSING,
    )

    expected_record_dict = create_data.dict()
    expected_record_dict.update(id=7)
    expected_data_result = result_data_schema(**expected_record_dict)
    expected_result = result_schema(data=expected_data_result)

    result = operation_function(create_data, interface)
    assert result.type == expected_result.type
    assert result.data == expected_result.data

    with pytest.raises(fastapi.HTTPException) as exc:
        operation_function(create_data, interface)
    assert exc.value.status_code == 303
