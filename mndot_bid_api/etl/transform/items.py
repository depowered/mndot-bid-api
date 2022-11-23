import pandas as pd
import pandera as pa

from mndot_bid_api.etl.types import RawItemsDF, TransformedItemsDF


@pa.check_types
def transform_items(raw_items: RawItemsDF, spec_year: str) -> TransformedItemsDF:
    df = pd.DataFrame()

    df["spec_code"] = raw_items["Item Number"].str.slice(0, 4)
    df["unit_code"] = raw_items["Item Number"].str.slice(5, 8)
    df["item_code"] = raw_items["Item Number"].str.slice(9, 14)
    df["short_description"] = (
        raw_items["Short Description"].str.strip().str.replace(";", ",")
    )
    df["long_description"] = (
        raw_items["Long Description"].str.strip().str.replace(";", ",")
    )
    df["unit"] = raw_items["Plan Unit Description"].str.strip()
    df["unit_abbreviation"] = raw_items["Unit Name"].str.strip().str.replace(" ", "")

    df[f"in_spec_{spec_year}"] = True

    return df
