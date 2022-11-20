import pandas as pd
import pandera as pa

from mndot_bid_api.etl.types import RawBiddersDF, TransformedBiddersDF


@pa.check_types
def transform_bidders(raw_bidders: RawBiddersDF) -> TransformedBiddersDF:
    ...
