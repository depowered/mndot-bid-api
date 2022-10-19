import fastapi
from mndot_bid_api.db import models
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
    # Get matching item record so that item_id can be assigned to the new bid record
    item_record = (
        db.query(models.Item)
        .filter(
            models.Item.spec_year == data.spec_year,
            models.Item.spec_code == data.spec_code,
            models.Item.unit_code == data.unit_code,
            models.Item.item_code == data.item_code,
        )
        .first()
    )

    if not item_record:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_404_NOT_FOUND,
            detail=f"Matching item not found for spec_year: {data.spec_year}, spec_code: {data.spec_code}, unit_code: {data.unit_code}, item_code: {data.item_code}. Cannot assign item_id.",
        )

    # Check if bid record already exists
    bid_record = (
        db.query(models.Bid)
        .filter(
            models.Bid.contract_id == data.contract_id,
            models.Bid.item_id == item_record.id,
            models.Bid.bidder_id == data.bidder_id,
        )
        .first()
    )

    if bid_record:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_303_SEE_OTHER,
            detail=f"Bid already exists at ID {bid_record.id}",
        )

    # BidCreateData properties don't match Bid model exactly, cannot unpack dict to create
    bid_model = models.Bid()
    setattr(bid_model, "contract_id", data.contract_id)
    setattr(bid_model, "item_id", item_record.id)
    setattr(bid_model, "bidder_id", data.bidder_id)
    setattr(bid_model, "quantity", data.quantity)
    setattr(bid_model, "unit_price", data.unit_price)
    setattr(bid_model, "bid_type", data.bid_type)

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
