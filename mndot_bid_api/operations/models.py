from datetime import date
from typing import Optional

from pydantic import BaseModel


class ContractCreateData(BaseModel):
    id: int
    letting_date: date
    sp_number: str
    district: str
    county: str
    description: str
    winning_bidder_id: int
    spec_year: str


class ContractResult(ContractCreateData):
    ...


class ContractUpdateData(BaseModel):
    id: int
    letting_date: Optional[date]
    sp_number: Optional[str]
    district: Optional[str]
    county: Optional[str]
    description: Optional[str]
    winning_bidder_id: Optional[int]
    spec_year: Optional[str]


class BidderCreateData(BaseModel):
    id: int
    name: str


class BidderResult(BidderCreateData):
    ...


class BidderUpdateData(BidderCreateData):
    ...


class BidCreateData(BaseModel):
    contract_id: int
    item_composite_id: str
    bidder_id: int
    quantity: float
    unit_price: int
    bid_type: str


class BidResult(BidCreateData):
    id: int


class BidUpdateData(BaseModel):
    id: int
    contract_id: Optional[int]
    item_composite_id: Optional[str]
    bidder_id: Optional[int]
    quantity: Optional[float]
    unit_price: Optional[int]
    bid_type: Optional[str]


class ItemCreateData(BaseModel):
    composite_id: str
    spec_year: str
    spec_code: str
    unit_code: str
    item_code: str
    short_description: str
    long_description: str
    unit: str
    unit_abreviation: str


class ItemResult(ItemCreateData):
    id: int


class ItemUpdateData(BaseModel):
    id: int
    composite_id: Optional[str]
    spec_year: Optional[str]
    spec_code: Optional[str]
    unit_code: Optional[str]
    item_code: Optional[str]
    short_description: Optional[str]
    long_description: Optional[str]
    unit: Optional[str]
    unit_abreviation: Optional[str]
