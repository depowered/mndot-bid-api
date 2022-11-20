from dataclasses import dataclass

import pandas as pd

from mndot_bid_api.etl.types import (
    FilePathOrBuffer,
    RawBiddersDF,
    RawBidsDF,
    RawContractDF,
)


@dataclass
class AbstractData:
    raw_contract: RawContractDF
    raw_bidders: RawBiddersDF
    raw_bids: RawBidsDF

    @property
    def contract_id(self) -> int:
        ...

    @property
    def winning_bidder_id(self) -> int:
        ...


def read_abstract_csv(filepath_or_buffer: FilePathOrBuffer) -> AbstractData:
    ...


def _read_contract_csv(csv_str: str) -> RawContractDF:
    ...


def _read_bidder_csv(csv_str: str) -> RawBiddersDF:
    ...


def _read_bid_csv(csv_str: str) -> RawBidsDF:
    ...
