import pytest

from mndot_bid_api import exceptions
from mndot_bid_api.etl.extract.abstract import read_abstract_csv
from mndot_bid_api.etl.transform.bidders import transform_bidders
from mndot_bid_api.schema import BidderCreateData

from .verify_columns_match_api import verify_columns_match_api


def test_transform_bidders(abstract_csv_content):
    abstract_data = read_abstract_csv(abstract_csv_content)
    input_df = abstract_data.raw_bidders
    api_create_schema = BidderCreateData

    df = transform_bidders(input_df)
    assert df.shape == (5, 2)

    matches_api = verify_columns_match_api(df, api_create_schema)
    assert matches_api is True

    invalid_input = input_df.drop(columns=input_df.columns[0])
    assert invalid_input.shape == (5, 1)
    with pytest.raises(exceptions.SchemaError):
        transform_bidders(invalid_input)
