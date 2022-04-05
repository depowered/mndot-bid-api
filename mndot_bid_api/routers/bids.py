from fastapi import APIRouter

from mndot_bid_api.operations.bids import read_bid, read_all_bids


router = APIRouter()


@router.get("/bids")
def api_read_all_bids():
    return read_all_bids()


@router.get("/bid/{bid_id}")
def api_read_bid(bid_id):
    return read_bid(bid_id)
