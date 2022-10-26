import fastapi
from mndot_bid_api.db import models
from mndot_bid_api.operations import schema
from sqlalchemy.orm import Session


def read_all_invalid_bids(db: Session) -> list[schema.InvalidBidResult]:
    invalid_bid_records = db.query(models.InvalidBid).all()
    return [
        schema.InvalidBidResult(**models.to_dict(invalid_bid))
        for invalid_bid in invalid_bid_records
    ]


def read_invalid_bid_by_id(invalid_bid_id: int, db: Session) -> schema.InvalidBidResult:

    invalid_bid_record = (
        db.query(models.InvalidBid)
        .filter(models.InvalidBid.id == invalid_bid_id)
        .first()
    )

    if not invalid_bid_record:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_404_NOT_FOUND,
            detail=f"Invalid bid record at ID {invalid_bid_id} not found",
        )

    return schema.InvalidBidResult(**models.to_dict(invalid_bid_record))


def create_invalid_bid(data: schema.InvalidBidCreateData, db: Session):

    query_filter = {key: value for key, value in data.dict().items()}
    invalid_bid_record = db.query(models.InvalidBid).filter_by(**query_filter).first()

    if invalid_bid_record:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_303_SEE_OTHER,
            detail=f"Invalid bid record already exists at ID {invalid_bid_record.id}",
        )

    invalid_bid_model = models.InvalidBid(**data.dict())

    db.add(invalid_bid_model)
    db.commit()

    return schema.InvalidBidResult(**models.to_dict(invalid_bid_model))


def update_invalid_bid(
    invalid_bid_id: int, data: schema.InvalidBidUpdateData, db: Session
) -> schema.InvalidBidResult:

    invalid_bid_record = (
        db.query(models.InvalidBid)
        .filter(models.InvalidBid.id == invalid_bid_id)
        .first()
    )

    if not invalid_bid_record:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_404_NOT_FOUND,
            detail=f"Invalid bid record at ID {invalid_bid_id} not found",
        )

    for key, value in data.dict(exclude_none=True).items():
        setattr(invalid_bid_record, key, value)

    db.add(invalid_bid_record)
    db.commit()

    return schema.InvalidBidResult(**models.to_dict(invalid_bid_record))


def delete_invalid_bid(invalid_bid_id: int, db: Session) -> None:

    invalid_bid_record = (
        db.query(models.InvalidBid)
        .filter(models.InvalidBid.id == invalid_bid_id)
        .first()
    )

    if not invalid_bid_record:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_404_NOT_FOUND,
            detail=f"Invalid bid record at ID {invalid_bid_id} not found",
        )

    db.delete(invalid_bid_record)
    db.commit()
