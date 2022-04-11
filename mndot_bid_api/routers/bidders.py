from fastapi import APIRouter

from mndot_bid_api.operations.bidders import create_bidder, read_bidder, update_bidder
from mndot_bid_api.operations.bidders import read_all_bidders
from mndot_bid_api.operations.models import (
    BidderCreateData,
    BidderResult,
    BidderUpdateData,
)


router = APIRouter()


@router.get("/bidders")
def api_read_all_bidders() -> list[BidderResult]:
    return read_all_bidders()


@router.get("/bidder/{bidder_id}")
def api_read_bidder(bidder_id: int) -> BidderResult:
    return read_bidder(bidder_id)


@router.post("/bidder")
def api_create_bidder(bidder: BidderCreateData) -> BidderResult:
    return create_bidder(bidder)


@router.put("/bidder/{bidder_id}")
def api_update_bidder(bidder_id: int, bidder: BidderUpdateData) -> BidderResult:
    return update_bidder(bidder_id, bidder)
