import pandas as pd
import pandera as pa

from mndot_bid_api.etl.types import RawContractDF, TransformedContractDF


@pa.check_types
def transform_contract(
    raw_contract: RawContractDF, winning_bidder_id: int
) -> TransformedContractDF:
    df = pd.DataFrame()

    df["id"] = raw_contract["Contract Id"].astype(int)
    df["letting_date"] = pd.to_datetime(raw_contract["Letting Date"])
    df["sp_number"] = raw_contract["SP Number"].str.strip()
    df["district"] = raw_contract["District"].str.strip().str.title()
    df["county"] = raw_contract["County"].str.strip().str.title()
    df["description"] = raw_contract["Job Description"].str.strip()
    df["winning_bidder_id"] = winning_bidder_id

    return df
