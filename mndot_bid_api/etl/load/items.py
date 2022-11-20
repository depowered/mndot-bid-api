import pandas as pd
import pandera as pa

from mndot_bid_api.etl.df_schemas import TransformedItems
from mndot_bid_api.etl.types import TransformedItemsDF
from mndot_bid_api.schema import LoadResult


@pa.check_input(TransformedItems.to_schema())
def load_items(transformed_items: TransformedItemsDF) -> list[LoadResult]:
    ...
