from typing import Optional

import pandas as pd
import pandera as pa
from pandera.typing import Series


class RawItems(pa.SchemaModel):
    item_number: Series[str] = pa.Field(alias="Item Number")
    short_description: Series[str] = pa.Field(alias="Short Description")
    long_description: Series[str] = pa.Field(alias="Long Description")
    unit_abbreviation: Series[str] = pa.Field(alias="Unit Name")
    unit: Series[str] = pa.Field(alias="Plan Unit Description")
    spec_year: Series[str] = pa.Field(alias="Spec Year")

    class Config:
        strict = "filter"  # drop columns not defined in schema


class TransformedItems(pa.SchemaModel):
    spec_code: Series[str]
    unit_code: Series[str]
    item_code: Series[str]
    short_description: Series[str]
    long_description: Series[str]
    unit: Series[str]
    unit_abbreviation: Series[str]
    in_spec_2016: Optional[Series[bool]]
    in_spec_2018: Optional[Series[bool]]
    in_spec_2020: Optional[Series[bool]]
    in_spec_2022: Optional[Series[bool]]

    @pa.check("[a-z]+_code", regex=True)
    @classmethod
    def verify_is_numeric(cls, series: Series[str]) -> Series[bool]:
        return series.str.isnumeric()

    @pa.check("[a-z]+_code", regex=True)
    @classmethod
    def verify_code_length(cls, series: Series[str]) -> Series[bool]:
        if series.name == "spec_code":
            return series.str.len().eq(4).all()
        if series.name == "unit_code":
            return series.str.len().eq(3).all()
        if series.name == "item_code":
            return series.str.len().eq(5).all()

    @pa.dataframe_check
    @classmethod
    def verify_in_spec_column_exists(cls, df: pd.DataFrame) -> bool:
        in_spec_columns = [
            "in_spec_2016",
            "in_spec_2018",
            "in_spec_2020",
            "in_spec_2022",
        ]
        return df.columns.isin(in_spec_columns).any()


class RawContract(pa.SchemaModel):
    letting_date: Series[str] = pa.Field(alias="Letting Date")
    job_description: Series[str] = pa.Field(alias="Job Description")
    contract_id: Series[str] = pa.Field(alias="Contract Id")
    sp_number: Series[str] = pa.Field(alias="SP Number")
    district: Series[str] = pa.Field(alias="District")
    county: Series[str] = pa.Field(alias="County")

    class Config:
        strict = "filter"  # drop columns not defined in schema


class TransformedContract(pa.SchemaModel):
    ...


class RawBidders(pa.SchemaModel):
    bidder_id: Series[str] = pa.Field(alias="Bidder Number")
    bidder_name: Series[str] = pa.Field(alias="Bidder Name")

    class Config:
        strict = "filter"  # drop columns not defined in schema


class TransformedBidders(pa.SchemaModel):
    id: Series[int]
    name: Series[str]


class RawBids(pa.SchemaModel):
    contract_id: Series[str] = pa.Field(alias="ContractId")
    item_number: Series[str] = pa.Field(alias="ItemNumber")
    item_description: Series[str] = pa.Field(alias="ItemDescription")
    quantity: Series[str] = pa.Field(alias="Quantity")
    unit_abbreviation: Series[str] = pa.Field(alias="UnitName")
    engineers_unit_price: Series[str] = pa.Field(alias="Engineers (Unit Price)")
    bidder_unit_price: Series[str] = pa.Field(alias=r"\d+\s\(Unit Price\)", regex=True)

    class Config:
        strict = "filter"  # drop columns not defined in schema


class TransformedBids(pa.SchemaModel):
    ...
