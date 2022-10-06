import fastapi
from mndot_bid_api.db import database, models
from mndot_bid_api.operations import schema
from sqlalchemy.orm import Session


def read_all_bids(db: Session) -> list[schema.BidResult]:
    bid_records = db.query(models.Bid).all()
    return [schema.BidResult(**models.to_dict(bid)) for bid in bid_records]


def read_bid(bid_id: int, db: Session) -> schema.BidResult:
    bid_record = db.query(models.Bid).filter(models.Bid.id == bid_id).first()
    if not bid_record:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_404_NOT_FOUND,
            detail=f"Bid at ID {bid_id} not found",
        )

    return schema.BidResult(**models.to_dict(bid_record))


def create_bid(data: schema.BidCreateData, db: Session) -> schema.BidResult:
    bid_record = (
        db.query(models.Bid)
        .filter(
            models.Bid.contract_id == data.contract_id,
            models.Bid.item_composite_id == data.item_composite_id,
            models.Bid.bidder_id == data.bidder_id,
        )
        .first()
    )
    if bid_record:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_303_SEE_OTHER,
            detail=f"Bid already exists at ID {bid_record.id}",
        )

    bid_model = models.Bid(**data.dict())
    db.add(bid_model)
    db.commit()

    return schema.BidResult(**models.to_dict(bid_model))


def update_bid(
    bid_id: int, data: schema.BidUpdateData, db: Session
) -> schema.BidResult:
    bid_record = db.query(models.Bid).filter(models.Bid.id == bid_id).first()
    if not bid_record:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_404_NOT_FOUND,
            detail=f"Bid at ID {bid_id} not found",
        )

    for key, value in data.dict(exclude_none=True).items():
        setattr(bid_record, key, value)

    db.add(bid_record)
    db.commit()

    return schema.BidResult(**models.to_dict(bid_record))


def delete_bid(bid_id: int, db: Session) -> None:
    bid_record = db.query(models.Bid).filter(models.Bid.id == bid_id).first()
    if not bid_record:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_404_NOT_FOUND,
            detail=f"Bid at ID {bid_id} not found",
        )

    db.delete(bid_record)
    db.commit()
