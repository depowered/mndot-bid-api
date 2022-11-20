import pandas as pd
import pandera as pa

from mndot_bid_api.etl.types import RawBidsDF, TransformedBidsDF


@pa.check_types
def transform_bids(raw_bids: RawBidsDF) -> TransformedBidsDF:
    ...
