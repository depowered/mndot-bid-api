from functools import partial

import pandas as pd
import pandera as pa

from mndot_bid_api.etl.types import RawBidsDF, TransformedBidsDF


@pa.check_types
def transform_bids(raw_bids: RawBidsDF, winning_bidder_id: int) -> TransformedBidsDF:
    df = pd.DataFrame()

    df["contract_id"] = raw_bids["ContractId"].astype(int)
    df["item_spec_code"] = raw_bids["ItemNumber"].str.strip().str.slice(0, 4)
    df["item_unit_code"] = raw_bids["ItemNumber"].str.strip().str.slice(4, 7)
    df["item_item_code"] = raw_bids["ItemNumber"].str.strip().str.slice(8)
    df["item_long_description"] = (
        raw_bids["ItemDescription"].str.strip().str.replace("''", '"')
    )
    df["item_unit_abbreviation"] = (
        raw_bids["UnitName"].str.strip().str.replace(" ", "").str.upper()
    )
    df["quantity"] = raw_bids["Quantity"].astype(float)

    # bidder_id for engineer is 0
    df["0"] = raw_bids["Engineers (Unit Price)"]

    # Filter for the bidder's unit prices
    bidder_unit_prices_df = raw_bids.filter(regex=r"\d+\s\(Unit Price\)")
    # Strip the column names to just bidder_id (str)
    renamed_bidder_unit_prices_df = bidder_unit_prices_df.rename(
        columns=_format_bidder_unit_price_column_name,
    )

    # Join the bidder's unit price colums to the partially transformed df
    df_with_bidder_unit_prices = pd.concat([df, renamed_bidder_unit_prices_df], axis=1)

    melt_df = df_with_bidder_unit_prices.melt(
        id_vars=[
            "contract_id",
            "item_spec_code",
            "item_unit_code",
            "item_item_code",
            "item_long_description",
            "item_unit_abbreviation",
            "quantity",
        ],
        var_name="bidder_id",
        value_name="unit_price",
    )
    # Format the the bidder_id as int
    melt_df["bidder_id"] = melt_df["bidder_id"].astype(int)
    # Format the values in the unit_price column
    melt_df["unit_price"] = melt_df["unit_price"].apply(_format_price)

    partial_assign_bid_type = partial(
        _assign_bid_type, winning_bidder_id=winning_bidder_id
    )

    melt_df["bid_type"] = (
        melt_df["bidder_id"].apply(partial_assign_bid_type).astype(str)
    )

    return melt_df


def _format_price(price: str) -> int:
    cleaned_str = price.strip().replace("$", "").replace(",", "")
    return int(float(cleaned_str) * 100)


def _format_bidder_unit_price_column_name(column_name: str) -> str:
    return column_name.strip().split(" ")[0]


def _assign_bid_type(bidder_id: int, winning_bidder_id: int) -> str:
    if bidder_id == 0:
        return "engineer"
    elif bidder_id == winning_bidder_id:
        return "winning"
    else:
        return "losing"
