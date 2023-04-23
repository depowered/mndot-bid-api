import pytest

from mndot_bid_api import exceptions
from mndot_bid_api.etl.df_schemas import TransformedBids
from mndot_bid_api.etl.extract.abstract import read_abstract_csv
from mndot_bid_api.etl.transform.bids import transform_bids
from mndot_bid_api.schema import BidCreateData

from .verify_columns_match_api import verify_columns_match_api


def test_transform_bids(abstract_csv_content):
    abstract_data = read_abstract_csv(abstract_csv_content)
    input_df = abstract_data.raw_bids
    winning_bidder_id = abstract_data.winning_bidder_id
    api_create_schema = BidCreateData

    df = transform_bids(input_df, winning_bidder_id, abstract_data.get_bidder_name_to_id_mapper())
    assert df.shape == (318, 10)

    matches_api = verify_columns_match_api(df, api_create_schema)
    assert matches_api is True

    invalid_input = input_df.drop(columns=input_df.columns[0])
    assert invalid_input.shape == (53, 10)
    with pytest.raises(exceptions.SchemaError):
        transform_bids(invalid_input, winning_bidder_id, abstract_data.get_bidder_name_to_id_mapper())

    # Test verify_is_numeric check raises
    non_numeric_code_df = df.copy()
    non_numeric_code_df.at[0, "item_spec_code"] = "abcd"
    with pytest.raises(exceptions.SchemaError):
        TransformedBids.validate(non_numeric_code_df)

    # Test verify_code_length check raises
    invalid_code_length_df = df.copy()
    invalid_code_length_df.at[0, "item_unit_code"] = "22"
    with pytest.raises(exceptions.SchemaError):
        TransformedBids.validate(invalid_code_length_df)

    # Test verify_value_in_district_enum raises
    invalid_unit_abbr = df.copy()
    invalid_unit_abbr.at[0, "item_unit_abbreviation"] = "ZZ"
    with pytest.raises(exceptions.SchemaError):
        TransformedBids.validate(invalid_unit_abbr)

    # Test verify_value_in_county_enum raises
    invalid_bid_type = df.copy()
    invalid_bid_type.at[0, "bid_type"] = "nope"
    with pytest.raises(exceptions.SchemaError):
        TransformedBids.validate(invalid_bid_type)
