import pandas as pd
import pandera as pa

from mndot_bid_api.etl.df_schemas import TransformedBids
from mndot_bid_api.etl.types import TransformedBidsDF
from mndot_bid_api.schema import LoadResult


@pa.check_input(TransformedBids.to_schema())
def load_bids(transformed_bids: TransformedBidsDF) -> list[LoadResult]:
    ...
