from fastapi import HTTPException
from sqlalchemy import select

from mndot_bid_api.db.engine import DBSession
from mndot_bid_api.db.models import DBBid, to_dict
from mndot_bid_api.operations.models import (
    BidCreateData,
    BidResult,
    BidUpdateData,
)


def read_all_bids() -> list[BidResult]:
    with DBSession() as session:
        statement = select(DBBid)
        bids: list[DBBid] = session.execute(statement).scalars().all()
        return [BidResult(**to_dict(b)) for b in bids]


def read_bid(bid_id) -> BidResult:
    with DBSession() as session:
        bid = session.get(DBBid, bid_id)
        if not bid:
            raise HTTPException(
                status_code=404, detail=f"Bid at ID {bid_id} not found."
            )
        return BidResult(**to_dict(bid))


def create_bid(data: BidCreateData) -> BidResult:
    with DBSession() as session:
        bid = DBBid(**data.dict())

        # verify that bid is not already in database before adding
        statement = (
            select(DBBid)
            .where(DBBid.item_number == bid.item_number)
            .where(DBBid.contract_id == bid.contract_id)
            .where(DBBid.bidder_id == bid.bidder_id)
        )
        selected_bid = session.execute(statement).scalar_one_or_none()
        if selected_bid:
            raise HTTPException(
                status_code=303, detail=f"Bid already exists at ID {selected_bid.id}."
            )

        session.add(bid)
        session.commit()
        return BidResult(**to_dict(bid))


def update_bid(bid_id: int, data: BidUpdateData) -> BidResult:
    with DBSession() as session:
        bid = session.get(DBBid, bid_id)

        # verify that bid is in database
        if not bid:
            raise HTTPException(
                status_code=404, detail=f"Bid at ID {bid_id} not found."
            )

        for key, value in data.dict(exclude_none=True).items():
            setattr(bid, key, value)

        session.commit()
        return BidResult(**to_dict(bid))
