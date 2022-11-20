import pandas as pd
import pandera as pa

from mndot_bid_api.etl.types import RawContractDF, TransformedContractDF


@pa.check_types
def transform_contract(raw_contract: RawContractDF) -> TransformedContractDF:
    ...
