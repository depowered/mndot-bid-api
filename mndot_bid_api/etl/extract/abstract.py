import re
from dataclasses import dataclass
from io import StringIO

import pandas as pd
import pandera as pa

from mndot_bid_api.etl.types import CSVContent, RawBiddersDF, RawBidsDF, RawContractDF


@dataclass
class AbstractData:
    raw_contract: RawContractDF
    raw_bidders: RawBiddersDF
    raw_bids: RawBidsDF

    @property
    def contract_id(self) -> int:
        return self.raw_contract.at[0, "Contract Id"]

    @property
    def winning_bidder_id(self) -> int:
        return self.raw_bidders.at[0, "Bidder Number"]


def read_abstract_csv(csv_str: CSVContent) -> AbstractData:

    contract_csv, bids_csv, bidders_csv = _split_csv(csv_str)

    raw_contract = _read_contract_csv(contract_csv)
    raw_bidders = _read_bidders_csv(bidders_csv)
    raw_bids = _read_bids_csv(bids_csv)

    return AbstractData(raw_contract, raw_bidders, raw_bids)


def _split_csv(csv_str: CSVContent) -> list[str]:
    """Splits the csv data by blank lines to divide into its three subtables."""
    blank_line_regex = r"(?:\r?\n){2,}"
    return re.split(blank_line_regex, csv_str)


@pa.check_types
def _read_contract_csv(csv_str: CSVContent) -> RawContractDF:
    return pd.read_csv(StringIO(csv_str), dtype="string", escapechar="\\")


@pa.check_types
def _read_bidders_csv(csv_str: CSVContent) -> RawBiddersDF:
    return pd.read_csv(StringIO(csv_str), dtype="string", escapechar="\\")


@pa.check_types
def _read_bids_csv(csv_content: CSVContent) -> RawBidsDF:
    return pd.read_csv(StringIO(csv_content), dtype="string", escapechar="\\")
