from sqlalchemy import select

from mndot_bid_api.db.engine import DBSession
from mndot_bid_api.db.models import DBBid, to_dict
from mndot_bid_api.operations.models import BidResult


def read_all_bids() -> list[BidResult]:
    with DBSession() as session:
        statement = select(DBBid)
        bids: list[DBBid] = session.execute(statement).scalars().all()
        return [BidResult(**to_dict(b)) for b in bids]


def read_bid(bid_id) -> BidResult:
    with DBSession() as session:
        bid = session.get(DBBid, bid_id)
        if not bid:
            return {"message": f"Bid with ID {bid_id} not found."}
        return BidResult(**to_dict(bid))
