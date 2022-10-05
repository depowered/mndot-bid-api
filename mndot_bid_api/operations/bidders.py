from fastapi import HTTPException, status
from mndot_bid_api.db import database, models
from mndot_bid_api.operations import schema
from sqlalchemy.orm import Session


def read_all_bidders(db: Session) -> list[schema.BidderResult]:
    bidder_models = db.query(models.Bidder).all()
    return [schema.BidderResult(**models.to_dict(model)) for model in bidder_models]


def read_bidder(bidder_id: int, db: Session) -> schema.BidderResult:
    bidder_model = db.query(models.Bidder).filter(models.Bidder.id == bidder_id).first()
    if not bidder_model:
        raise HTTPException(
            status_code=404, detail=f"Bidder at ID {bidder_id} not found."
        )
    return schema.BidderResult(**models.to_dict(bidder_model))


def create_bidder(data: schema.BidderCreateData, db: Session) -> schema.BidderResult:
    # Verify record is not already present
    record = db.query(models.Bidder).filter(models.Bidder.id == data.id).first()
    if record:
        raise HTTPException(
            status_code=303, detail=f"Bidder already exists at ID {data.id}"
        )

    bidder_model = models.Bidder(**data.dict())
    db.add(bidder_model)
    db.commit()

    return schema.BidderResult(**models.to_dict(bidder_model))


def update_bidder(
    bidder_id: int, data: schema.BidderUpdateData, db: Session
) -> schema.BidderResult:
    # Verify record exists
    record = db.query(models.Bidder).filter(models.Bidder.id == bidder_id).first()
    if not record:
        raise HTTPException(
            status_code=404, detail=f"Bidder at ID {bidder_id} not found."
        )

    for key, value in data.dict(exclude_none=True).items():
        setattr(record, key, value)

    db.add(record)
    db.commit()

    return schema.BidderResult(**models.to_dict(record))


def delete_bidder(bidder_id: int, db: Session) -> None:
    # Verify record exists
    record = db.query(models.Bidder).filter(models.Bidder.id == bidder_id).first()
    if not record:
        raise HTTPException(
            status_code=404, detail=f"Bidder at ID {bidder_id} not found."
        )

    db.delete(record)
    db.commit()
