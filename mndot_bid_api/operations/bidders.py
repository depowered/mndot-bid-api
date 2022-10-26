import fastapi
from mndot_bid_api.db import models
from mndot_bid_api.operations import schema
from sqlalchemy.orm import Session


def read_all_bidders(db: Session) -> list[schema.BidderResult]:
    bidder_records = db.query(models.Bidder).all()
    return [schema.BidderResult(**models.to_dict(model)) for model in bidder_records]


def read_bidder(bidder_id: int, db: Session) -> schema.BidderResult:
    bidder_record = (
        db.query(models.Bidder).filter(models.Bidder.id == bidder_id).first()
    )
    if not bidder_record:
        raise fastapi.HTTPException(
            status_code=404, detail=f"Bidder at ID {bidder_id} not found."
        )
    return schema.BidderResult(**models.to_dict(bidder_record))


def create_bidder(data: schema.BidderCreateData, db: Session) -> schema.BidderResult:
    bidder_record = db.query(models.Bidder).filter(models.Bidder.id == data.id).first()
    if bidder_record:
        raise fastapi.HTTPException(
            status_code=303, detail=f"Bidder already exists at ID {data.id}"
        )

    bidder_model = models.Bidder(**data.dict())
    db.add(bidder_model)
    db.commit()

    return schema.BidderResult(**models.to_dict(bidder_model))


def update_bidder(
    bidder_id: int, data: schema.BidderUpdateData, db: Session
) -> schema.BidderResult:
    bidder_record = (
        db.query(models.Bidder).filter(models.Bidder.id == bidder_id).first()
    )
    if not bidder_record:
        raise fastapi.HTTPException(
            status_code=404, detail=f"Bidder at ID {bidder_id} not found."
        )

    for key, value in data.dict(exclude_none=True).items():
        setattr(bidder_record, key, value)

    db.add(bidder_record)
    db.commit()

    return schema.BidderResult(**models.to_dict(bidder_record))


def delete_bidder(bidder_id: int, db: Session) -> None:
    bidder_record = (
        db.query(models.Bidder).filter(models.Bidder.id == bidder_id).first()
    )
    if not bidder_record:
        raise fastapi.HTTPException(
            status_code=404, detail=f"Bidder at ID {bidder_id} not found."
        )

    db.delete(bidder_record)
    db.commit()
