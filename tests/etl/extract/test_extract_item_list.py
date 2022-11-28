import pytest

from mndot_bid_api import exceptions
from mndot_bid_api.etl import df_schemas
from mndot_bid_api.etl.extract import item_list


def test_read_item_list_csv(item_list_csv_content):
    item_list_data = item_list.read_item_list_csv(item_list_csv_content)
    df = item_list_data.raw_items.copy()

    assert df.shape == (8032, 6)
    df_schemas.RawItems.validate(df)

    assert item_list_data.spec_year == "2018"

    invalid_df = df.drop(columns="Spec Year")
    with pytest.raises(exceptions.SchemaError):
        df_schemas.RawItems.validate(invalid_df)


def test_read_item_list_csv_raises(abstract_csv_content):
    with pytest.raises(exceptions.ParserError):
        item_list.read_item_list_csv(abstract_csv_content)
