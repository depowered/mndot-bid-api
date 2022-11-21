import pandera as pa
import pytest

from mndot_bid_api.etl import df_schemas
from mndot_bid_api.etl.extract import item_list


def test_read_item_list_csv(item_list_csv_content):
    item_list_data = item_list.read_item_list_csv(item_list_csv_content)

    assert item_list_data.raw_items.shape == (7713, 6)
    df_schemas.RawItems.validate(item_list_data.raw_items)

    assert item_list_data.spec_year == "2016"
