from typing import Callable

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
    schema.BidderCollection
    | schema.ContractCollection
    | schema.ItemCollection
    | schema.BidCollection
    | schema.InvalidBidCollection
)


def generic_read_all_test(
    interface: CRUDInterface,
    result_data_schema: ResultDataSchemaType,
    result_schema: ResultSchemaType,
    sample_data: list[dict],
    operation_function: Callable,
) -> None:

    expected_result_data = [
        result_data_schema(**record_dict) for record_dict in sample_data
    ]
    expected_result = result_schema(data=expected_result_data)

    # Test valid limit
    limit = 100
    result = operation_function(limit, interface)
    assert result.type == expected_result.type
    assert len(result.data) == len(expected_result.data)
    for item in result.data:
        assert item in expected_result.data

    # Test limit of zero returns all records
    limit = 0
    result = operation_function(limit, interface)
    assert len(result.data) == len(expected_result.data)

    # Test negative limit returns no records
    limit = -500
    result = operation_function(limit, interface)
    assert len(result.data) == 0


def test_read_all_bidders(configured_sessionmaker: sessionmaker):
    model = models.Bidder
    interface = DBModelInterface(model, configured_sessionmaker)
    result_data_schema = schema.BidderResult
    result_schema = schema.BidderCollection
    sample_data = sample_record_dicts.sample_bidders
    operation_function = operations.bidders.read_all_bidders

    generic_read_all_test(
        interface,
        result_data_schema,
        result_schema,
        sample_data,
        operation_function,
    )


def test_read_all_contracts(configured_sessionmaker: sessionmaker):
    model = models.Contract
    interface = DBModelInterface(model, configured_sessionmaker)
    result_data_schema = schema.ContractResult
    result_schema = schema.ContractCollection
    sample_data = sample_record_dicts.sample_contracts
    operation_function = operations.contracts.read_all_contracts

    generic_read_all_test(
        interface,
        result_data_schema,
        result_schema,
        sample_data,
        operation_function,
    )


def test_read_all_items(configured_sessionmaker: sessionmaker):
    model = models.Item
    interface = DBModelInterface(model, configured_sessionmaker)
    result_data_schema = schema.ItemResult
    result_schema = schema.ItemCollection
    sample_data = sample_record_dicts.sample_items
    operation_function = operations.items.read_all_items

    generic_read_all_test(
        interface,
        result_data_schema,
        result_schema,
        sample_data,
        operation_function,
    )


def test_read_all_bids(configured_sessionmaker: sessionmaker):
    model = models.Bid
    interface = DBModelInterface(model, configured_sessionmaker)
    result_data_schema = schema.BidResult
    result_schema = schema.BidCollection
    sample_data = sample_record_dicts.sample_bids
    operation_function = operations.bids.read_all_bids

    generic_read_all_test(
        interface,
        result_data_schema,
        result_schema,
        sample_data,
        operation_function,
    )


def test_read_all_invalid_bids(configured_sessionmaker: sessionmaker):
    model = models.InvalidBid
    interface = DBModelInterface(model, configured_sessionmaker)
    result_data_schema = schema.InvalidBidResult
    result_schema = schema.InvalidBidCollection
    sample_data = sample_record_dicts.sample_invalid_bids
    operation_function = operations.invalid_bids.read_all_invalid_bids

    generic_read_all_test(
        interface,
        result_data_schema,
        result_schema,
        sample_data,
        operation_function,
    )
