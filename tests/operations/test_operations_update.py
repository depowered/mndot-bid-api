from typing import Callable

import fastapi
import pytest
from sqlalchemy.orm import sessionmaker

from mndot_bid_api import operations, schema
from mndot_bid_api.db import models
from mndot_bid_api.db.interface import DBModelInterface
from mndot_bid_api.operations.crud_interface import CRUDInterface
from tests.data import sample_record_dicts

UpdateDataSchemaType = (
    schema.BidderUpdateData
    | schema.ContractUpdateData
    | schema.ItemUpdateData
    | schema.BidUpdateData
    | schema.InvalidBidUpdateData
)

ResultSchemaType = (
    schema.Bidder | schema.Contract | schema.Item | schema.Bid | schema.InvalidBid
)


def generic_update_test(
    operation_function: Callable,
    id: int,
    update_data: UpdateDataSchemaType,
    interface: CRUDInterface,
    expected_result: ResultSchemaType,
) -> None:

    result = operation_function(id, update_data, interface)
    assert result.type == expected_result.type
    assert result.data == expected_result.data

    with pytest.raises(fastapi.HTTPException) as exc:
        operation_function(-7, update_data, interface)
    assert exc.value.status_code == 404


def test_update_bidder(configured_sessionmaker: sessionmaker):
    model = models.Bidder
    interface = DBModelInterface(model, configured_sessionmaker)
    result_data_schema = schema.BidderResult
    result_schema = schema.Bidder
    sample_data = sample_record_dicts.sample_bidders[1]
    id = sample_data["id"]
    operation_function = operations.bidders.update_bidder

    update_data = schema.BidderUpdateData(name="Name has changed")

    expected_data_result = result_data_schema(**sample_data)
    expected_data_result.name = "Name has changed"
    expected_result = result_schema(data=expected_data_result)

    generic_update_test(operation_function, id, update_data, interface, expected_result)


def test_update_contracts(configured_sessionmaker: sessionmaker):
    model = models.Contract
    interface = DBModelInterface(model, configured_sessionmaker)
    result_data_schema = schema.ContractResult
    result_schema = schema.Contract
    sample_data = sample_record_dicts.sample_contracts[0]
    id = sample_data["id"]
    operation_function = operations.contracts.update_contract

    update_data = schema.ContractUpdateData(sp_number="1234-56")

    expected_data_result = result_data_schema(**sample_data)
    expected_data_result.sp_number = "1234-56"
    expected_result = result_schema(data=expected_data_result)

    generic_update_test(operation_function, id, update_data, interface, expected_result)


def test_update_items(configured_sessionmaker: sessionmaker):
    model = models.Item
    interface = DBModelInterface(model, configured_sessionmaker)
    result_data_schema = schema.ItemResult
    result_schema = schema.Item
    sample_data = sample_record_dicts.sample_items[0]
    id = sample_data["id"]
    operation_function = operations.items.update_item

    update_data = schema.ItemUpdateData(spec_code="9999")

    expected_data_result = result_data_schema(**sample_data)
    expected_data_result.spec_code = "9999"
    expected_result = result_schema(data=expected_data_result)

    generic_update_test(operation_function, id, update_data, interface, expected_result)


def test_update_bids(configured_sessionmaker: sessionmaker):
    model = models.Bid
    interface = DBModelInterface(model, configured_sessionmaker)
    result_data_schema = schema.BidResult
    result_schema = schema.Bid
    sample_data = sample_record_dicts.sample_bids[0]
    id = sample_data["id"]
    operation_function = operations.bids.update_bid

    update_data = schema.BidUpdateData(unit_price=1_000_000_00)

    expected_data_result = result_data_schema(**sample_data)
    expected_data_result.unit_price = 1_000_000_00
    expected_result = result_schema(data=expected_data_result)

    generic_update_test(operation_function, id, update_data, interface, expected_result)


def test_update_invalid_bids(configured_sessionmaker: sessionmaker):
    model = models.InvalidBid
    interface = DBModelInterface(model, configured_sessionmaker)
    result_data_schema = schema.InvalidBidResult
    result_schema = schema.InvalidBid
    sample_data = sample_record_dicts.sample_invalid_bids[0]
    id = sample_data["id"]
    operation_function = operations.invalid_bids.update_invalid_bid

    update_data = schema.InvalidBidUpdateData(unit_price=1_000_000_00)

    expected_data_result = result_data_schema(**sample_data)
    expected_data_result.unit_price = 1_000_000_00
    expected_result = result_schema(data=expected_data_result)

    generic_update_test(operation_function, id, update_data, interface, expected_result)
