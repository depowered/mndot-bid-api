import pandas as pd
import pandera as pa
from pandera.typing import Series


class RawItems(pa.SchemaModel):
    ...


class TransformedItems(pa.SchemaModel):
    ...


class RawContract(pa.SchemaModel):
    letting_date: Series[pd.StringDtype] = pa.Field(alias="Letting Date")
    job_description: Series[pd.StringDtype] = pa.Field(alias="Job Description")
    contract_id: Series[pd.StringDtype] = pa.Field(alias="Contract Id")
    sp_number: Series[pd.StringDtype] = pa.Field(alias="SP Number")
    district: Series[pd.StringDtype] = pa.Field(alias="District")
    county: Series[pd.StringDtype] = pa.Field(alias="County")


class TransformedContract(pa.SchemaModel):
    ...


class RawBidders(pa.SchemaModel):
    bidder_id: Series[pd.StringDtype] = pa.Field(alias="Bidder Number")
    bidder_name: Series[pd.StringDtype] = pa.Field(alias="Bidder Name")

    class Config:
        strict = "filter"  # drop columns not defined in schema


class TransformedBidders(pa.SchemaModel):
    ...


class RawBids(pa.SchemaModel):
    contract_id: Series[pd.StringDtype] = pa.Field(alias="ContractId")
    item_number: Series[pd.StringDtype] = pa.Field(alias="ItemNumber")
    item_description: Series[pd.StringDtype] = pa.Field(alias="ItemDescription")
    quantity: Series[pd.StringDtype] = pa.Field(alias="Quantity")
    unit_abbreviation: Series[pd.StringDtype] = pa.Field(alias="UnitName")
    engineers_unit_price: Series[pd.StringDtype] = pa.Field(
        alias="Engineers (Unit Price)"
    )
    bidder_unit_price: Series[pd.StringDtype] = pa.Field(
        alias=r"\d+\s\(Unit Price\)", regex=True
    )

    class Config:
        strict = "filter"  # drop columns not defined in schema


class TransformedBids(pa.SchemaModel):
    ...
