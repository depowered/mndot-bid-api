from typing import Callable

import fastapi
import pytest
from sqlalchemy.orm import sessionmaker

from mndot_bid_api import operations
from mndot_bid_api.db import models
from mndot_bid_api.db.interface import DBModelInterface
from mndot_bid_api.operations import schema
from mndot_bid_api.operations.crud_interface import CRUDInterface
from tests.data import sample_record_dicts

ResultDataSchemaType = (
    schema.BidderResult
    | schema.ContractResult
    | schema.ItemResult
    | schema.BidResult
    | schema.InvalidBidResult
)

ResultSchemaType = (
    schema.Bidder | schema.Contract | schema.Item | schema.Bid | schema.InvalidBid
)


def generic_read_by_id_test(
    id: int,
    interface: CRUDInterface,
    result_data_schema: ResultDataSchemaType,
    result_schema: ResultSchemaType,
    sample_data: dict,
    operation_function: Callable,
) -> None:

    expected_result_data = result_data_schema(**sample_data)
    expected_result = result_schema(data=expected_result_data)

    result = operation_function(id, interface)
    assert result.type == expected_result.type
    assert result.data == expected_result.data

    with pytest.raises(fastapi.HTTPException) as exc:
        operation_function(-7, interface)
    assert exc.value.status_code == 404


def test_read_by_id_bidders(configured_sessionmaker: sessionmaker):
    model = models.Bidder
    interface = DBModelInterface(model, configured_sessionmaker)
    result_data_schema = schema.BidderResult
    result_schema = schema.Bidder
    sample_data = sample_record_dicts.sample_bidders[1]
    id = sample_data["id"]
    operation_function = operations.bidders.read_bidder

    generic_read_by_id_test(
        id,
        interface,
        result_data_schema,
        result_schema,
        sample_data,
        operation_function,
    )


def test_read_by_id_contracts(configured_sessionmaker: sessionmaker):
    model = models.Contract
    interface = DBModelInterface(model, configured_sessionmaker)
    result_data_schema = schema.ContractResult
    result_schema = schema.Contract
    sample_data = sample_record_dicts.sample_contracts[0]
    id = sample_data["id"]
    operation_function = operations.contracts.read_contract

    generic_read_by_id_test(
        id,
        interface,
        result_data_schema,
        result_schema,
        sample_data,
        operation_function,
    )


def test_read_by_id_items(configured_sessionmaker: sessionmaker):
    model = models.Item
    interface = DBModelInterface(model, configured_sessionmaker)
    result_data_schema = schema.ItemResult
    result_schema = schema.Item
    sample_data = sample_record_dicts.sample_items[0]
    id = sample_data["id"]
    operation_function = operations.items.read_item_by_id

    generic_read_by_id_test(
        id,
        interface,
        result_data_schema,
        result_schema,
        sample_data,
        operation_function,
    )


def test_read_by_id_bids(configured_sessionmaker: sessionmaker):
    model = models.Bid
    interface = DBModelInterface(model, configured_sessionmaker)
    result_data_schema = schema.BidResult
    result_schema = schema.Bid
    sample_data = sample_record_dicts.sample_bids[0]
    id = sample_data["id"]
    operation_function = operations.bids.read_bid

    generic_read_by_id_test(
        id,
        interface,
        result_data_schema,
        result_schema,
        sample_data,
        operation_function,
    )


def test_read_by_id_invalid_bids(configured_sessionmaker: sessionmaker):
    model = models.InvalidBid
    interface = DBModelInterface(model, configured_sessionmaker)
    result_data_schema = schema.InvalidBidResult
    result_schema = schema.InvalidBid
    sample_data = sample_record_dicts.sample_invalid_bids[0]
    id = sample_data["id"]
    operation_function = operations.invalid_bids.read_invalid_bid_by_id

    generic_read_by_id_test(
        id,
        interface,
        result_data_schema,
        result_schema,
        sample_data,
        operation_function,
    )
