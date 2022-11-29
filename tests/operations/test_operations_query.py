from typing import Callable

import fastapi
import pytest
from sqlalchemy.orm import sessionmaker

from mndot_bid_api import operations, schema
from mndot_bid_api.db import models
from mndot_bid_api.db.interface import DBModelInterface
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


def generic_query_test(
    interface: CRUDInterface,
    result_data_schema: ResultDataSchemaType,
    result_schema: ResultSchemaType,
    sample_data: list[dict],
    operation_function: Callable,
    query_kwargs: dict,
) -> None:
    expected_result_data = [
        result_data_schema(**sample_dict) for sample_dict in sample_data
    ]
    expected_result = result_schema(data=expected_result_data)

    # Test with high limit; expect all records
    result = operation_function(interface, limit=100, **query_kwargs)
    assert result.type == expected_result.type
    assert result.data == expected_result.data

    # Test with positive limit; expect one record
    result = operation_function(interface, limit=1, **query_kwargs)
    assert len(result.data) == 1

    # Test with negative limit; expect no records
    result = operation_function(interface, limit=-1, **query_kwargs)
    assert len(result.data) == 0

    # Test no kwargs raises
    with pytest.raises(fastapi.HTTPException) as exc:
        operation_function(interface, limit=100)
    assert exc.value.status_code == 400

    # Test invalid kwarg value raises
    with pytest.raises(fastapi.HTTPException) as exc:
        operation_function(interface, limit=100, id=-7)
    assert exc.value.status_code == 404


def test_query_bidder(configured_sessionmaker: sessionmaker):
    model = models.Bidder
    interface = DBModelInterface(model, configured_sessionmaker)
    result_data_schema = schema.BidderResult
    result_schema = schema.BidderCollection
    sample_data = [sample_record_dicts.sample_bidders[1]]
    operation_function = operations.bidders.query_bidder

    query_kwargs = {"name": sample_data[0]["name"]}

    generic_query_test(
        interface,
        result_data_schema,
        result_schema,
        sample_data,
        operation_function,
        query_kwargs,
    )


def test_query_contracts(configured_sessionmaker: sessionmaker):
    model = models.Contract
    interface = DBModelInterface(model, configured_sessionmaker)
    result_data_schema = schema.ContractResult
    result_schema = schema.ContractCollection
    sample_data = [sample_record_dicts.sample_contracts[0]]
    operation_function = operations.contracts.query_contract

    query_kwargs = {"sp_number": sample_data[0]["sp_number"]}

    generic_query_test(
        interface,
        result_data_schema,
        result_schema,
        sample_data,
        operation_function,
        query_kwargs,
    )


def test_query_items(configured_sessionmaker: sessionmaker):
    model = models.Item
    interface = DBModelInterface(model, configured_sessionmaker)
    result_data_schema = schema.ItemResult
    result_schema = schema.ItemCollection
    sample_data = sample_record_dicts.sample_items
    operation_function = operations.items.query_item

    query_kwargs = {"in_spec_2018": sample_data[0]["in_spec_2018"]}

    generic_query_test(
        interface,
        result_data_schema,
        result_schema,
        sample_data,
        operation_function,
        query_kwargs,
    )


def test_query_bids(configured_sessionmaker: sessionmaker):
    model = models.Bid
    interface = DBModelInterface(model, configured_sessionmaker)
    result_data_schema = schema.BidResult
    result_schema = schema.BidCollection
    sample_data = sample_record_dicts.sample_bids[:6]
    operation_function = operations.bids.query_bid

    query_kwargs = {"item_id": sample_data[0]["item_id"]}

    generic_query_test(
        interface,
        result_data_schema,
        result_schema,
        sample_data,
        operation_function,
        query_kwargs,
    )


def test_query_invalid_bids(configured_sessionmaker: sessionmaker):
    model = models.InvalidBid
    interface = DBModelInterface(model, configured_sessionmaker)
    result_data_schema = schema.InvalidBidResult
    result_schema = schema.InvalidBidCollection
    sample_data = sample_record_dicts.sample_invalid_bids
    operation_function = operations.invalid_bids.query_invalid_bid

    query_kwargs = {"item_long_description": sample_data[0]["item_long_description"]}

    generic_query_test(
        interface,
        result_data_schema,
        result_schema,
        sample_data,
        operation_function,
        query_kwargs,
    )
