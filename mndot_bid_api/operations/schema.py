from datetime import date
from typing import Optional

from mndot_bid_api.operations import enums
from pydantic import BaseModel, constr


class ContractCreateData(BaseModel):
    id: int
    letting_date: date
    sp_number: str
    district: enums.District
    county: enums.County
    description: str
    winning_bidder_id: int
    spec_year: constr(strip_whitespace=True, min_length=4, max_length=4)


class ContractResult(BaseModel):
    id: int
    letting_date: date
    sp_number: str
    district: str
    county: str
    description: str
    winning_bidder_id: int
    spec_year: str


class ContractUpdateData(BaseModel):
    letting_date: Optional[date]
    sp_number: Optional[str]
    district: Optional[enums.District]
    county: Optional[enums.County]
    description: Optional[str]
    winning_bidder_id: Optional[int]
    spec_year: Optional[str]


class BidderCreateData(BaseModel):
    id: int
    name: str


class BidderResult(BidderCreateData):
    pass


class BidderUpdateData(BaseModel):
    name: str


class BidCreateData(BaseModel):
    contract_id: int
    item_composite_id: str
    bidder_id: int
    quantity: float
    unit_price: int
    bid_type: enums.BidType


class BidResult(BaseModel):
    id: int
    contract_id: int
    item_composite_id: str
    bidder_id: int
    quantity: float
    unit_price: int
    bid_type: str


class BidUpdateData(BaseModel):
    contract_id: Optional[int]
    item_composite_id: Optional[str]
    bidder_id: Optional[int]
    quantity: Optional[float]
    unit_price: Optional[int]
    bid_type: Optional[enums.BidType]


class ItemCreateData(BaseModel):
    spec_year: enums.SpecYear
    spec_code: constr(strip_whitespace=True, min_length=4, max_length=4)
    unit_code: constr(strip_whitespace=True, min_length=3, max_length=3)
    item_code: constr(strip_whitespace=True, min_length=5, max_length=5)
    short_description: constr(strip_whitespace=True, to_upper=True)
    long_description: constr(strip_whitespace=True, to_upper=True)
    unit: enums.Unit
    unit_abbreviation: enums.UnitAbbreviation

    @property
    def composite_id(self) -> str:
        return "_".join([str(self.spec_code), str(self.unit_code), str(self.item_code)])


class ItemResult(BaseModel):
    id: int
    composite_id: str
    spec_year: str
    spec_code: str
    unit_code: str
    item_code: str
    short_description: str
    long_description: str
    unit: str
    unit_abbreviation: str


class ItemUpdateData(BaseModel):
    spec_year: Optional[enums.SpecYear]
    spec_code: Optional[constr(strip_whitespace=True, min_length=4, max_length=4)]
    unit_code: Optional[constr(strip_whitespace=True, min_length=3, max_length=3)]
    item_code: Optional[constr(strip_whitespace=True, min_length=5, max_length=5)]
    short_description: Optional[constr(strip_whitespace=True, to_upper=True)]
    long_description: Optional[constr(strip_whitespace=True, to_upper=True)]
    unit: Optional[enums.Unit]
    unit_abbreviation: Optional[enums.UnitAbbreviation]

    @property
    def composite_id(self) -> str:
        return "_".join([str(self.spec_code), str(self.unit_code), str(self.item_code)])
