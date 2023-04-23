import re
from dataclasses import dataclass
from io import StringIO

import pandas as pd

from mndot_bid_api import exceptions
from mndot_bid_api.etl.df_schemas import RawBidders, RawBids, RawContract
from mndot_bid_api.etl.types import (CSVContent, RawBiddersDF, RawBidsDF,
                                     RawContractDF)


@dataclass
class AbstractData:
    raw_contract: RawContractDF
    raw_bidders: RawBiddersDF
    raw_bids: RawBidsDF

    @property
    def contract_id(self) -> int:
        return int(self.raw_contract.at[0, "Contract Id"])

    @property
    def winning_bidder_id(self) -> int:
        return int(self.raw_bidders.at[0, "Bidder Number"])

    def get_bidder_name_to_id_mapper(self) -> dict[str, str]:
        mapper = dict()
        for row in self.raw_bidders.to_dict("records"):
            bidder_name = row["Bidder Name"]
            key = f"{bidder_name} (Unit Price) "
            value = str(int(row["Bidder Number"])) # cast to int to strip leading zeros then back to str
            mapper[key] = value
        return mapper


def read_abstract_csv(csv_content: CSVContent) -> AbstractData:

    contract_csv, bids_csv, bidders_csv = _split_csv(csv_content)

    raw_contract = _read_contract_csv(contract_csv)
    raw_bidders = _read_bidders_csv(bidders_csv)
    raw_bids = _read_bids_csv(bids_csv)

    return AbstractData(raw_contract, raw_bidders, raw_bids)


def _split_csv(csv_content: CSVContent) -> list[str]:
    """Splits the csv data by blank lines to divide into its three subtables."""
    blank_line_regex = r"(?:\r?\n){2,}"
    split_content = re.split(blank_line_regex, csv_content)

    if len(split_content) != 3:
        raise exceptions.ParseAbstractCSVError("Failed to split absract csv content.")

    return re.split(blank_line_regex, csv_content)


def _read_contract_csv(csv_content: CSVContent) -> RawContractDF:
    df = pd.read_csv(StringIO(csv_content), dtype=str, escapechar="\\")
    return RawContract.validate(df)


def _read_bidders_csv(csv_content: CSVContent) -> RawBiddersDF:
    df = pd.read_csv(StringIO(csv_content), dtype=str, escapechar="\\")
    return RawBidders.validate(df)


def _read_bids_csv(csv_content: CSVContent) -> RawBidsDF:
    df = pd.read_csv(StringIO(csv_content), dtype=str, escapechar="\\")
    return RawBids.validate(df)
