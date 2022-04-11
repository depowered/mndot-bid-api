from datetime import date
from typing import Optional
from pydantic import BaseModel


class ContractResult(BaseModel):
    id: int
    is_processed: bool
    let_date: Optional[date]
    let_year: Optional[int]
    spec_year: Optional[int]
    sp_number: Optional[str]
    district: Optional[str]
    county: Optional[str]
    engineers_total: Optional[int]
    lowest_bidder_id: Optional[int]
    lowest_bidder_total: Optional[int]


class ContractCreateData(BaseModel):
    id: int
    is_processed: bool = False
    let_date: date
    let_year: Optional[int]
    spec_year: Optional[int]
    sp_number: str
    district: str
    county: str
    engineers_total: int
    lowest_bidder_id: int
    lowest_bidder_total: int


class ContractUpdateData(BaseModel):
    is_processed: Optional[bool]
    let_date: Optional[date]
    let_year: Optional[int]
    spec_year: Optional[int]
    sp_number: Optional[str]
    district: Optional[str]
    county: Optional[str]
    engineers_total: Optional[int]
    lowest_bidder_id: Optional[int]
    lowest_bidder_total: Optional[int]


class BidderResult(BaseModel):
    id: int
    name: Optional[str]


class BidderCreateData(BaseModel):
    id: int
    name: Optional[str]


class BidderUpdateData(BaseModel):
    name: str


class BidResult(BaseModel):
    id: int
    item_number: str
    spec_year: int
    quantity: float
    unit_price: int
    total_price: int
    contract_id: int
    bidder_id: int
    bidder_rank: int


class BidCreateData(BaseModel):
    item_number: str
    spec_year: int
    quantity: float
    unit_price: int
    total_price: int
    contract_id: int
    bidder_id: int
    bidder_rank: int


class BidUpdateData(BaseModel):
    item_number: Optional[str]
    spec_year: Optional[int]
    quantity: Optional[float]
    unit_price: Optional[int]
    total_price: Optional[int]
    contract_id: Optional[int]
    bidder_id: Optional[int]
    bidder_rank: Optional[int]
