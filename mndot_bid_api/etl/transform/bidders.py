import pandas as pd
import pandera as pa

from mndot_bid_api.etl.types import RawBiddersDF, TransformedBiddersDF


@pa.check_types
def transform_bidders(raw_bidders: RawBiddersDF) -> TransformedBiddersDF:
    df = pd.DataFrame()

    df["id"] = raw_bidders["Bidder Number"].astype(int)
    df["name"] = raw_bidders["Bidder Name"].str.strip()

    return df
