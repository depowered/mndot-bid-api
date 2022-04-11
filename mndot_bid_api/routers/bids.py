from fastapi import APIRouter

from mndot_bid_api.operations.bids import (
    create_bid,
    read_bid,
    read_all_bids,
    update_bid,
)
from mndot_bid_api.operations.models import BidCreateData, BidResult, BidUpdateData


router = APIRouter()


@router.get("/bids")
def api_read_all_bids():
    return read_all_bids()


@router.get("/bid/{bid_id}")
def api_read_bid(bid_id):
    return read_bid(bid_id)


@router.post("/bid")
def api_create_bid(data: BidCreateData) -> BidResult:
    return create_bid(data)


@router.put("/bid/{bid_id}")
def api_update_bid(bid_id: int, data: BidUpdateData) -> BidResult:
    return update_bid(bid_id, data)
