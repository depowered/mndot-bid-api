from sqlalchemy.orm import sessionmaker

from mndot_bid_api.db import models
from mndot_bid_api.db.interface import DBModelInterface
from mndot_bid_api.etl.extract.item_list import read_item_list_csv
from mndot_bid_api.etl.load.items import load_items
from mndot_bid_api.etl.transform.items import transform_items


def test_load_items_not_in_db(
    item_list_csv_content: str, configured_sessionmaker: sessionmaker
):
    # Setup CRUD Interface
    interface = DBModelInterface(models.Item, configured_sessionmaker)

    # Extract and transforme data
    item_list_data = read_item_list_csv(item_list_csv_content)
    transformed_df = transform_items(item_list_data.raw_items, item_list_data.spec_year)

    # Filter transformed data for bids with matching items in the test database
    # 2011/601/01000 AS BUILT & 2106.507/00010 EXCAVATION - COMMON
    existing_items_df = transformed_df.query(
        "long_description == 'AS BUILT' or long_description == 'EXCAVATION - COMMON'"
    )
    assert existing_items_df.shape == (2, 8)

    # Delete all existing item entries
    interface.delete(1)
    interface.delete(2)

    # Load the data
    load_results = load_items(existing_items_df, interface)

    assert len(load_results) == 2
    for result in load_results:
        assert result.model == "Item"
        assert result.operation == "create"
        assert result.status_code == 201
        assert result.message is None
        assert result.input_data is not None
        assert result.record_data is not None


def test_load_items_already_in_db(
    item_list_csv_content: str, configured_sessionmaker: sessionmaker
):
    # Setup CRUD Interface
    interface = DBModelInterface(models.Item, configured_sessionmaker)

    # Extract and transforme data
    item_list_data = read_item_list_csv(item_list_csv_content)
    transformed_df = transform_items(item_list_data.raw_items, item_list_data.spec_year)

    # Filter transformed data for bids with matching items in the test database
    # 2011/601/01000 AS BUILT & 2106.507/00010 EXCAVATION - COMMON
    existing_items_df = transformed_df.query(
        "long_description == 'AS BUILT' or long_description == 'EXCAVATION - COMMON'"
    )
    assert existing_items_df.shape == (2, 8)

    # Load the data
    load_results = load_items(existing_items_df, interface)

    assert len(load_results) == 2
    for result in load_results:
        assert result.model == "Item"
        assert result.operation == "update"
        assert result.status_code == 200
        assert result.message.startswith("Item already exists at ID")
        assert result.input_data is not None
        assert result.record_data is not None


def test_load_items_counts(
    item_list_csv_content: str, configured_sessionmaker: sessionmaker
):
    # Setup CRUD Interface
    interface = DBModelInterface(models.Item, configured_sessionmaker)

    # Extract and transforme data
    item_list_data = read_item_list_csv(item_list_csv_content)
    transformed_df = transform_items(item_list_data.raw_items, item_list_data.spec_year)

    assert transformed_df.shape == (8032, 8)

    # Load the data
    load_results = load_items(transformed_df, interface)

    assert len(load_results) == 8032

    # Count the status codes in the LoadResults list
    status_201_count = 0
    status_200_count = 0
    for result in load_results:
        if result.status_code == 201:
            status_201_count += 1
        if result.status_code == 200:
            status_200_count += 1

    assert status_200_count == 2
    assert status_201_count == 8030

    # The database should have the same number of item records as the transformed df
    db_item_record_count = len(interface.read_all())
    assert db_item_record_count == 8032
