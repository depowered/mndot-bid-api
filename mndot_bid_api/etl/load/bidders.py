import pandas as pd
import pandera as pa

from mndot_bid_api.etl.df_schemas import TransformedBidders
from mndot_bid_api.etl.types import TransformedBiddersDF
from mndot_bid_api.schema import LoadResult


@pa.check_input(TransformedBidders.to_schema())
def load_bidders(transformed_bidders: TransformedBiddersDF) -> list[LoadResult]:
    ...
