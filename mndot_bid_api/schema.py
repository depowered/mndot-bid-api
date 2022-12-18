from datetime import date

from pydantic import BaseModel, constr

from mndot_bid_api import enums


class ContractCreateData(BaseModel):
    id: int
    letting_date: date
    sp_number: str
    district: enums.District
    county: enums.County
    description: str
    winning_bidder_id: int


class ContractResult(BaseModel):
    id: int
    letting_date: date
    sp_number: str
    district: str
    county: str
    description: str
    winning_bidder_id: int


class ContractUpdateData(BaseModel):
    letting_date: date | None
    sp_number: str | None
    district: enums.District | None
    county: enums.County | None
    description: str | None
    winning_bidder_id: int | None


class Contract(BaseModel):
    type: str = "Contract"
    data: ContractResult


class ContractCollection(BaseModel):
    type: str = "ContractCollection"
    data: list[ContractResult]


class ContractLoadResult(BaseModel):
    model: str = "Contract"
    operation: str
    status_code: int | None = None
    message: str | None = None
    input_data: ContractCreateData
    record_data: Contract | None = None


#############################################################################


class BidderCreateData(BaseModel):
    id: int
    name: str


class BidderResult(BaseModel):
    id: int
    name: str | None


class BidderUpdateData(BaseModel):
    name: str


class Bidder(BaseModel):
    type: str = "Bidder"
    data: BidderResult


class BidderCollection(BaseModel):
    type: str = "BidderCollection"
    data: list[BidderResult]


class BidderLoadResult(BaseModel):
    model: str = "Bidder"
    operation: str
    status_code: int | None = None
    message: str | None = None
    input_data: BidderCreateData
    record_data: Bidder | None = None


#############################################################################


class BidCreateData(BaseModel):
    contract_id: int
    bidder_id: int
    item_spec_code: constr(strip_whitespace=True, min_length=4, max_length=4)
    item_unit_code: constr(strip_whitespace=True, min_length=3, max_length=3)
    item_item_code: constr(strip_whitespace=True, min_length=5, max_length=5)
    item_long_description: constr(strip_whitespace=True, to_upper=True)
    item_unit_abbreviation: constr(strip_whitespace=True, to_upper=True)
    quantity: float
    unit_price: int
    bid_type: enums.BidType


class BidResult(BaseModel):
    id: int
    contract_id: int
    bidder_id: int
    item_id: int
    quantity: float
    unit_price: int
    bid_type: str


class BidUpdateData(BaseModel):
    contract_id: int | None
    bidder_id: int | None
    item_id: int | None
    quantity: float | None
    unit_price: int | None
    bid_type: enums.BidType | None


class Bid(BaseModel):
    type: str = "Bid"
    data: BidResult


class BidCollection(BaseModel):
    type: str = "BidCollection"
    data: list[BidResult]


class BidLoadResult(BaseModel):
    model: str = "Bid"
    operation: str
    status_code: int | None = None
    message: str | None = None
    input_data: BidCreateData
    record_data: Bid | None = None


#############################################################################


class InvalidBidResult(BaseModel):
    id: int
    contract_id: int
    bidder_id: int
    item_spec_code: str
    item_unit_code: str
    item_item_code: str
    item_long_description: str
    item_unit_abbreviation: str
    quantity: float
    unit_price: int
    bid_type: enums.BidType


class InvalidBidUpdateData(BaseModel):
    contract_id: int | None
    bidder_id: int | None
    item_spec_code: constr(strip_whitespace=True, min_length=4, max_length=4) | None
    item_unit_code: constr(strip_whitespace=True, min_length=3, max_length=3) | None
    item_item_code: constr(strip_whitespace=True, min_length=5, max_length=5) | None
    item_long_description: constr(strip_whitespace=True, to_upper=True) | None
    item_unit_abbreviation: constr(strip_whitespace=True, to_upper=True) | None
    quantity: float | None
    unit_price: int | None
    bid_type: enums.BidType | None


class InvalidBid(BaseModel):
    type: str = "InvalidBid"
    data: InvalidBidResult


class InvalidBidCollection(BaseModel):
    type: str = "InvalidBidCollection"
    data: list[InvalidBidResult]


class InvalidBidLoadResult(BaseModel):
    model: str = "InvalidBid"
    operation: str
    status_code: int | None = None
    message: str | None = None
    input_data: BidCreateData
    record_data: InvalidBid | None = None


#############################################################################


class ItemCreateData(BaseModel):
    spec_code: constr(strip_whitespace=True, min_length=4, max_length=4)
    unit_code: constr(strip_whitespace=True, min_length=3, max_length=3)
    item_code: constr(strip_whitespace=True, min_length=5, max_length=5)
    short_description: constr(strip_whitespace=True, to_upper=True)
    long_description: constr(strip_whitespace=True, to_upper=True)
    unit: enums.Unit
    unit_abbreviation: enums.UnitAbbreviation
    in_spec_2016: bool | None
    in_spec_2018: bool | None
    in_spec_2020: bool | None
    in_spec_2022: bool | None


class ItemResult(BaseModel):
    id: int
    spec_code: str
    unit_code: str
    item_code: str
    short_description: str
    long_description: str
    unit: str
    unit_abbreviation: str
    in_spec_2016: bool
    in_spec_2018: bool
    in_spec_2020: bool
    in_spec_2022: bool


class ItemUpdateData(BaseModel):
    spec_code: constr(strip_whitespace=True, min_length=4, max_length=4) | None
    unit_code: constr(strip_whitespace=True, min_length=3, max_length=3) | None
    item_code: constr(strip_whitespace=True, min_length=5, max_length=5) | None
    short_description: constr(strip_whitespace=True, to_upper=True) | None
    long_description: constr(strip_whitespace=True, to_upper=True) | None
    unit: enums.Unit | None
    unit_abbreviation: enums.UnitAbbreviation | None
    in_spec_2016: bool | None
    in_spec_2018: bool | None
    in_spec_2020: bool | None
    in_spec_2022: bool | None


class Item(BaseModel):
    type: str = "Item"
    data: ItemResult


class ItemCollection(BaseModel):
    type: str = "ItemCollection"
    data: list[ItemResult]


class ItemLoadResult(BaseModel):
    model: str
    operation: str
    status_code: int | None = None
    message: str | None = None
    input_data: ItemCreateData
    record_data: Item | None = None


#############################################################################


class ItemListETL(BaseModel):
    spec_year: str
    item_results: list[ItemLoadResult]


class AbstractETL(BaseModel):
    contract_id: int
    contract_results: list[ContractLoadResult]
    bidder_results: list[BidderLoadResult]
    bid_results: list[BidLoadResult | InvalidBidLoadResult]


#############################################################################


class WeightedAvgUnitPrice(BaseModel):
    item_id: int
    year: int
    bid_type: enums.BidType
    weighted_avg_unit_price: float
    occurances: int
