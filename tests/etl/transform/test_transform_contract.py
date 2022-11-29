import pytest

from mndot_bid_api import exceptions
from mndot_bid_api.etl.df_schemas import TransformedContract
from mndot_bid_api.etl.extract.abstract import read_abstract_csv
from mndot_bid_api.etl.transform.contract import transform_contract
from mndot_bid_api.schema import ContractCreateData

from .verify_columns_match_api import verify_columns_match_api


def test_transform_contract(abstract_csv_content):
    abstract_data = read_abstract_csv(abstract_csv_content)
    input_df = abstract_data.raw_contract
    winning_bidder_id = abstract_data.winning_bidder_id
    api_create_schema = ContractCreateData

    df = transform_contract(input_df, winning_bidder_id)
    assert df.shape == (1, 7)

    matches_api = verify_columns_match_api(df, api_create_schema)
    assert matches_api is True

    invalid_input = input_df.drop(columns=input_df.columns[0])
    assert invalid_input.shape == (1, 5)
    with pytest.raises(exceptions.SchemaError):
        transform_contract(invalid_input, winning_bidder_id)

    # Test verify_value_in_district_enum raises
    invalid_district = df.copy()
    invalid_district.at[0, "district"] = "abc"
    with pytest.raises(exceptions.SchemaError):
        TransformedContract.validate(invalid_district)

    # Test verify_value_in_county_enum raises
    invalid_county = df.copy()
    invalid_county.at[0, "county"] = "abc"
    with pytest.raises(exceptions.SchemaError):
        TransformedContract.validate(invalid_county)
