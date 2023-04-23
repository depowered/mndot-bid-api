import pytest

from mndot_bid_api import exceptions
from mndot_bid_api.etl import df_schemas
from mndot_bid_api.etl.extract import abstract


def test_split_csv(abstract_csv_content: str):
    split_csv = abstract._split_csv(abstract_csv_content)

    assert isinstance(split_csv, list)
    assert len(split_csv) == 3
    assert split_csv[0].startswith('"Letting Date"')
    assert split_csv[1].startswith('"ContractId"')
    assert split_csv[2].startswith('"Bidder Number"')


def test_split_csv_raises(item_list_csv_content: str):
    with pytest.raises(exceptions.ParseAbstractCSVError):
        abstract._split_csv(item_list_csv_content)


def test_read_contract_csv(abstract_csv_content: str):
    split_csv = abstract._split_csv(abstract_csv_content)
    contract_content = split_csv[0]
    df = abstract._read_contract_csv(contract_content)

    assert df.shape == (1, 6)
    df_schemas.RawContract.validate(df)

    invalid_df = df.drop(columns="Letting Date")
    assert invalid_df.shape == (1, 5)
    with pytest.raises(exceptions.SchemaError):
        df_schemas.RawContract.validate(invalid_df)


def test_read_bids_csv(abstract_csv_content: str):
    split_csv = abstract._split_csv(abstract_csv_content)
    bids_content = split_csv[1]
    df = abstract._read_bids_csv(bids_content)

    assert df.shape == (53, 11)
    df_schemas.RawBids.validate(df)

    invalid_df = df.drop(columns="UnitName")
    assert invalid_df.shape == (53, 10)
    with pytest.raises(exceptions.SchemaError):
        df_schemas.RawBids.validate(invalid_df)


def test_read_bidders_csv(abstract_csv_content: str):
    split_csv = abstract._split_csv(abstract_csv_content)
    bidders_content = split_csv[2]
    df = abstract._read_bidders_csv(bidders_content)

    assert df.shape == (5, 2)
    df_schemas.RawBidders.validate(df)

    invalid_df = df.drop(columns="Bidder Name")
    assert invalid_df.shape == (5, 1)
    with pytest.raises(exceptions.SchemaError):
        df_schemas.RawBidders.validate(invalid_df)


def test_read_abstract_csv(abstract_csv_content):
    abstract_data = abstract.read_abstract_csv(abstract_csv_content)

    assert abstract_data.raw_contract.shape == (1, 6)
    df_schemas.RawContract.validate(abstract_data.raw_contract)

    assert abstract_data.raw_bids.shape == (53, 11)
    df_schemas.RawBids.validate(abstract_data.raw_bids)

    assert abstract_data.raw_bidders.shape == (5, 2)
    df_schemas.RawBidders.validate(abstract_data.raw_bidders)

    assert abstract_data.contract_id == 220005
    assert abstract_data.winning_bidder_id == 207897
