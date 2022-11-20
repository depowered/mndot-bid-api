import pandas as pd
import pandera as pa

from mndot_bid_api.etl.df_schemas import TransformedContract
from mndot_bid_api.etl.types import TransformedContractDF
from mndot_bid_api.schema import LoadResult


@pa.check_input(TransformedContract.to_schema())
def load_contract(transformed_contract: TransformedContractDF) -> list[LoadResult]:
    ...
