from fastapi import HTTPException
from sqlalchemy import select

from mndot_bid_api.db.engine import DBSession
from mndot_bid_api.db.models import DBBidder, to_dict
from mndot_bid_api.operations.models import (
    BidderResult,
    BidderCreateData,
    BidderUpdateData,
)


def read_all_bidders() -> list[BidderResult]:
    with DBSession() as session:
        statement = select(DBBidder)
        bidders = session.execute(statement).scalars().all()
        return [BidderResult(**to_dict(b)) for b in bidders]


def read_bidder(bidder_id) -> BidderResult:
    with DBSession() as session:
        bidder = session.get(DBBidder, bidder_id)
        if not bidder:
            raise HTTPException(
                status_code=404, detail=f"Bidder at ID {bidder_id} not found."
            )
        return BidderResult(**to_dict(bidder))


def create_bidder(data: BidderCreateData) -> BidderResult:
    with DBSession() as session:
        bidder = DBBidder(**data.dict())

        # verify that bidder is not already in database before adding
        selected_bidder = session.get(DBBidder, bidder.id)
        if selected_bidder:
            raise HTTPException(
                status_code=303,
                detail=f"Bidder already exists at ID {selected_bidder.id}.",
            )

        session.add(bidder)
        session.commit()
        return BidderResult(**to_dict(bidder))


def update_bidder(bidder_id: int, data: BidderUpdateData) -> BidderResult:
    with DBSession() as session:
        bidder: DBBidder = session.get(DBBidder, bidder_id)

        if not bidder:
            raise HTTPException(
                status_code=404, detail=f"Bidder at ID {bidder_id} not found."
            )

        for key, value in data.dict(exclude_none=True).items():
            setattr(bidder, key, value)

        session.commit()
        return BidderResult(**to_dict(bidder))
