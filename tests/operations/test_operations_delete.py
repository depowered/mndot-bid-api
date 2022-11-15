from typing import Callable

import fastapi
import pytest
from sqlalchemy.orm import sessionmaker

from mndot_bid_api import operations
from mndot_bid_api.db import models
from mndot_bid_api.db.interface import DBModelInterface
from mndot_bid_api.operations.crud_interface import CRUDInterface
from tests.data import sample_record_dicts


def generic_delete_test(
    operation_function: Callable, id: int, interface: CRUDInterface
) -> None:
    try:
        operation_function(id, interface)
    except Exception as exc:
        assert (
            False
        ), f"delete_bidder raised an unexpected execption: {type(exc).__name__}"

    with pytest.raises(fastapi.HTTPException) as exc:
        operation_function(-7, interface)
    assert exc.value.status_code == 404


def test_delete_bidders(configured_sessionmaker: sessionmaker):
    model = models.Bidder
    interface = DBModelInterface(model, configured_sessionmaker)
    sample_data = sample_record_dicts.sample_bidders[1]
    id = sample_data["id"]
    operation_function = operations.bidders.delete_bidder

    generic_delete_test(operation_function, id, interface)


def test_delete_contracts(configured_sessionmaker: sessionmaker):
    model = models.Contract
    interface = DBModelInterface(model, configured_sessionmaker)
    sample_data = sample_record_dicts.sample_contracts[0]
    id = sample_data["id"]
    operation_function = operations.contracts.delete_contract

    generic_delete_test(operation_function, id, interface)


def test_delete_items(configured_sessionmaker: sessionmaker):
    model = models.Item
    interface = DBModelInterface(model, configured_sessionmaker)
    sample_data = sample_record_dicts.sample_items[0]
    id = sample_data["id"]
    operation_function = operations.items.delete_item

    generic_delete_test(operation_function, id, interface)


def test_delete_bids(configured_sessionmaker: sessionmaker):
    model = models.Bid
    interface = DBModelInterface(model, configured_sessionmaker)
    sample_data = sample_record_dicts.sample_bids[0]
    id = sample_data["id"]
    operation_function = operations.items.delete_item

    generic_delete_test(operation_function, id, interface)


def test_delete_invalid_bids(configured_sessionmaker: sessionmaker):
    model = models.InvalidBid
    interface = DBModelInterface(model, configured_sessionmaker)
    sample_data = sample_record_dicts.sample_invalid_bids[0]
    id = sample_data["id"]
    operation_function = operations.items.delete_item

    generic_delete_test(operation_function, id, interface)
