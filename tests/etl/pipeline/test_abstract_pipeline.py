import pytest

from mndot_bid_api import exceptions
from mndot_bid_api.db import models
from mndot_bid_api.db.interface import DBModelInterface
from mndot_bid_api.etl.pipeline.abstract import abstract_etl_pipeline


def test_abstract_etl_pipeline(abstract_csv_file, configured_sessionmaker):
    # Setup CRUD Interfaces
    contract_interface = DBModelInterface(models.Contract, configured_sessionmaker)
    bid_interface = DBModelInterface(models.Bid, configured_sessionmaker)
    invalid_bid_interface = DBModelInterface(models.InvalidBid, configured_sessionmaker)
    bidder_interface = DBModelInterface(models.Bidder, configured_sessionmaker)
    item_interface = DBModelInterface(models.Item, configured_sessionmaker)

    abstract_etl = abstract_etl_pipeline(
        abstract_csv_file,
        contract_interface,
        bid_interface,
        invalid_bid_interface,
        bidder_interface,
        item_interface,
    )

    assert abstract_etl.contract_id == 220005
    assert len(abstract_etl.contract_results) == 1
    assert len(abstract_etl.bid_results) == 318
    assert len(abstract_etl.bidder_results) == 5


def test_abstract_etl_pipeline_raises(item_list_csv_file, configured_sessionmaker):
    # Setup CRUD Interfaces
    contract_interface = DBModelInterface(models.Contract, configured_sessionmaker)
    bid_interface = DBModelInterface(models.Bid, configured_sessionmaker)
    invalid_bid_interface = DBModelInterface(models.InvalidBid, configured_sessionmaker)
    bidder_interface = DBModelInterface(models.Bidder, configured_sessionmaker)
    item_interface = DBModelInterface(models.Item, configured_sessionmaker)

    with pytest.raises(exceptions.HTTPException) as err:
        abstract_etl_pipeline(
            item_list_csv_file,
            contract_interface,
            bid_interface,
            invalid_bid_interface,
            bidder_interface,
            item_interface,
        )
    assert err.value.status_code == 422
    assert err.value.detail["error"] == "ParserError"
