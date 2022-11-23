import pandera as pa
import pytest

from mndot_bid_api.etl.df_schemas import TransformedItems
from mndot_bid_api.etl.extract.item_list import read_item_list_csv
from mndot_bid_api.etl.transform.items import transform_items
from mndot_bid_api.schema import ItemCreateData

from .verify_columns_match_api import verify_columns_match_api


def test_transform_items(item_list_csv_content):
    item_list_data = read_item_list_csv(item_list_csv_content)
    input_df = item_list_data.raw_items
    spec_year = item_list_data.spec_year
    api_create_schema = ItemCreateData

    df = transform_items(input_df, spec_year)
    assert df.shape == (7713, 8)

    # Test pa.check_types raises on invalid input
    invalid_input = input_df.drop(columns=input_df.columns[0])
    assert invalid_input.shape == (7713, 5)
    with pytest.raises(pa.errors.SchemaError):
        transform_items(invalid_input, spec_year)

    # Test verify_is_numeric check raises
    non_numeric_code_df = df.copy()
    non_numeric_code_df["spec_code"][0] = "abcd"
    with pytest.raises(pa.errors.SchemaError):
        TransformedItems.validate(non_numeric_code_df)

    # Test verify_code_length check raises
    invalid_code_length_df = df.copy()
    invalid_code_length_df["unit_code"][0] = "22"
    with pytest.raises(pa.errors.SchemaError):
        TransformedItems.validate(invalid_code_length_df)

    # Test verify_code_length check raises
    invalid_code_length_df = df.copy()
    invalid_code_length_df["unit_code"][0] = "22"
    with pytest.raises(pa.errors.SchemaError):
        TransformedItems.validate(invalid_code_length_df)

    # Test verify_value_in_unit_enum check raises
    invalid_unit_df = df.copy()
    invalid_unit_df["unit"][0] = "NOT A UNIT"
    with pytest.raises(pa.errors.SchemaError):
        TransformedItems.validate(invalid_unit_df)

    # Test verify_value_in_unit_enum check raises
    invalid_unit_abbr_df = df.copy()
    invalid_unit_abbr_df["unit_abbreviation"][0] = "NOT A UNIT"
    with pytest.raises(pa.errors.SchemaError):
        TransformedItems.validate(invalid_unit_abbr_df)

    # Test verify_in_spec_column_exists check raises
    missing_in_spec_column = df.drop(columns="in_spec_2016")
    with pytest.raises(pa.errors.SchemaError):
        TransformedItems.validate(missing_in_spec_column)

    # TODO: verify_columns_match_api isn't compatible with optional columns
    # matches_api = verify_columns_match_api(df, api_create_schema)
    # assert matches_api is True
