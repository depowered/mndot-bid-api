import pandera as pa
import pytest

from mndot_bid_api.etl import df_schemas
from mndot_bid_api.etl.extract import item_list


def test_read_item_list_csv(item_list_csv_content):
    item_list_data = item_list.read_item_list_csv(item_list_csv_content)
    df = item_list_data.raw_items.copy()

    assert df.shape == (7713, 6)
    df_schemas.RawItems.validate(df)

    assert item_list_data.spec_year == "2016"

    invalid_df = df.drop(columns="Spec Year")
    with pytest.raises(pa.errors.SchemaError):
        df_schemas.RawItems.validate(invalid_df)
