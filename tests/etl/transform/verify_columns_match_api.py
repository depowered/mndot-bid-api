import pandas as pd

from mndot_bid_api import schema

APICreateSchema = (
    schema.BidCreateData
    | schema.BidderCreateData
    | schema.ContractCreateData
    | schema.ItemCreateData
)


def verify_columns_match_api(
    df: pd.DataFrame, api_create_schema: APICreateSchema
) -> bool:
    """Checks if the transformed dataframe matches the corresponding ModelCreateData schema."""
    columns: list[str] = sorted(list(df.columns))

    api_create_fields: list[str] = sorted(
        [field for field in api_create_schema.__fields__.keys()]
    )

    return columns == api_create_fields
