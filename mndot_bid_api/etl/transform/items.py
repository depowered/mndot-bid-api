import pandas as pd
import pandera as pa

from mndot_bid_api.etl.types import RawItemsDF, TransformedItemsDF


@pa.check_types
def transform_items(raw_items: RawItemsDF) -> TransformedItemsDF:
    ...
