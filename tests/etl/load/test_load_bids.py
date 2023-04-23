from sqlalchemy.orm import sessionmaker

from mndot_bid_api.db import models
from mndot_bid_api.db.interface import DBModelInterface
from mndot_bid_api.etl.extract.abstract import read_abstract_csv
from mndot_bid_api.etl.load.bids import load_bids
from mndot_bid_api.etl.transform.bids import transform_bids


def test_load_valid_bids_not_in_db(
    abstract_csv_content: str, configured_sessionmaker: sessionmaker
):
    # Setup CRUD Interface
    bid_interface = DBModelInterface(models.Bid, configured_sessionmaker)
    item_interface = DBModelInterface(models.Item, configured_sessionmaker)
    invalid_bid_interface = DBModelInterface(models.InvalidBid, configured_sessionmaker)

    # Extract and transform data
    abstract_data = read_abstract_csv(abstract_csv_content)
    transformed_df = transform_bids(
        abstract_data.raw_bids, abstract_data.winning_bidder_id, abstract_data.get_bidder_name_to_id_mapper()
    )

    # Filter transformed data for bids with matching items in the test database
    # 2011/601/01000 AS BUILT & 2106.507/00010 EXCAVATION - COMMON
    valid_bids_df = transformed_df.query(
        "item_long_description == 'AS BUILT' or item_long_description == 'EXCAVATION - COMMON'"
    )
    assert valid_bids_df.shape == (12, 10)

    # Delete all existing bid entries
    for id in range(1, 13):
        bid_interface.delete(id)

    # Load the data
    load_results = load_bids(
        valid_bids_df, bid_interface, item_interface, invalid_bid_interface
    )
    assert len(load_results) == 12
    for load_result in load_results:
        assert load_result.model == "Bid"
        assert load_result.status_code == 201
        assert load_result.message is None
        assert load_result.input_data is not None
        assert load_result.record_data is not None


def test_load_valid_bids_already_in_db(
    abstract_csv_content: str, configured_sessionmaker: sessionmaker
):
    # Setup CRUD Interface
    bid_interface = DBModelInterface(models.Bid, configured_sessionmaker)
    item_interface = DBModelInterface(models.Item, configured_sessionmaker)
    invalid_bid_interface = DBModelInterface(models.InvalidBid, configured_sessionmaker)

    # Extract and transform data
    abstract_data = read_abstract_csv(abstract_csv_content)
    transformed_df = transform_bids(
        abstract_data.raw_bids, abstract_data.winning_bidder_id, abstract_data.get_bidder_name_to_id_mapper()
    )

    # Filter transformed data for bids with matching items in the test database
    # 2011/601/01000 AS BUILT & 2106.507/00010 EXCAVATION - COMMON
    valid_bids_df = transformed_df.query(
        "item_long_description == 'AS BUILT' or item_long_description == 'EXCAVATION - COMMON'"
    )
    assert valid_bids_df.shape == (12, 10)

    # Load the data
    load_results = load_bids(
        valid_bids_df, bid_interface, item_interface, invalid_bid_interface
    )
    assert len(load_results) == 12
    for load_result in load_results:
        assert load_result.model == "Bid"
        assert load_result.status_code == 303
        assert load_result.message.startswith("Bid already exists at ID")
        assert load_result.input_data is not None
        assert load_result.record_data is None


def test_load_invalid_bids_not_in_db(
    abstract_csv_content: str, configured_sessionmaker: sessionmaker
):
    # Setup CRUD Interface
    bid_interface = DBModelInterface(models.Bid, configured_sessionmaker)
    item_interface = DBModelInterface(models.Item, configured_sessionmaker)
    invalid_bid_interface = DBModelInterface(models.InvalidBid, configured_sessionmaker)

    # Extract and transform data
    abstract_data = read_abstract_csv(abstract_csv_content)
    transformed_df = transform_bids(
        abstract_data.raw_bids, abstract_data.winning_bidder_id, abstract_data.get_bidder_name_to_id_mapper()
    )

    # Filter transformed data for a subset of bids without matching items in the test database
    # 2021.501/00010 MOBILIZATION & 2031.502/00010 FIELD OFFICE
    invalid_bids_df = transformed_df.query(
        "item_long_description == 'MOBILIZATION' or item_long_description == 'FIELD OFFICE'"
    )
    assert invalid_bids_df.shape == (12, 10)

    # Load the data
    load_results = load_bids(
        invalid_bids_df, bid_interface, item_interface, invalid_bid_interface
    )
    assert len(load_results) == 12
    for load_result in load_results:
        assert load_result.model == "InvalidBid"
        assert load_result.status_code == 201
        assert load_result.message.startswith("No matching item found.")
        assert load_result.input_data is not None
        assert load_result.record_data is not None


def test_load_invalid_bids_already_in_db(
    abstract_csv_content: str, configured_sessionmaker: sessionmaker
):
    # Setup CRUD Interface
    bid_interface = DBModelInterface(models.Bid, configured_sessionmaker)
    item_interface = DBModelInterface(models.Item, configured_sessionmaker)
    invalid_bid_interface = DBModelInterface(models.InvalidBid, configured_sessionmaker)

    # Extract and transform data
    abstract_data = read_abstract_csv(abstract_csv_content)
    transformed_df = transform_bids(
        abstract_data.raw_bids, abstract_data.winning_bidder_id, abstract_data.get_bidder_name_to_id_mapper()
    )

    # Filter transformed data for a subset of bids with matching items in the test database
    # but already exist as InvalidBid entries in the test database
    # 2564.502/00200 INSTALL SIGN
    invalid_bids_df = transformed_df.query("item_long_description == 'INSTALL SIGN'")
    assert invalid_bids_df.shape == (6, 10)

    # Load the data
    load_results = load_bids(
        invalid_bids_df, bid_interface, item_interface, invalid_bid_interface
    )
    assert len(load_results) == 6
    for load_result in load_results:
        assert load_result.model == "InvalidBid"
        assert load_result.status_code == 303
        assert load_result.message.startswith(
            "No matching item found. Redirect to create invalid bid. Invalid Bid already exists at ID"
        )
        assert load_result.input_data is not None
        assert load_result.record_data is None


def test_load_bids_counts(
    abstract_csv_content: str, configured_sessionmaker: sessionmaker
):
    # Setup CRUD Interface
    bid_interface = DBModelInterface(models.Bid, configured_sessionmaker)
    item_interface = DBModelInterface(models.Item, configured_sessionmaker)
    invalid_bid_interface = DBModelInterface(models.InvalidBid, configured_sessionmaker)

    # Extract and transform data
    abstract_data = read_abstract_csv(abstract_csv_content)
    transformed_df = transform_bids(
        abstract_data.raw_bids, abstract_data.winning_bidder_id, abstract_data.get_bidder_name_to_id_mapper()
    )

    assert transformed_df.shape == (318, 10)

    # Load the data
    load_results = load_bids(
        transformed_df, bid_interface, item_interface, invalid_bid_interface
    )

    assert len(load_results) == 318

    # Count the model values in the LoadResults list
    bid_model_count = 0
    invalid_bid_model_count = 0
    for result in load_results:
        if result.model == "Bid":
            bid_model_count += 1
        if result.model == "InvalidBid":
            invalid_bid_model_count += 1

    assert bid_model_count == 12
    assert invalid_bid_model_count == 306

    # The database record counts for each table should match as well
    db_bid_record_count = len(bid_interface.read_all())
    assert db_bid_record_count == 12
    db_invalid_bid_record_count = len(invalid_bid_interface.read_all())
    assert db_invalid_bid_record_count == 306
