import fastapi
from mndot_bid_api.db import models
from mndot_bid_api.operations import schema
from sqlalchemy.orm import Session


def read_all_items(db: Session) -> list[schema.ItemResult]:
    item_records = db.query(models.Item).all()
    return [schema.ItemResult(**models.to_dict(item)) for item in item_records]


def read_item(item_id: int, db: Session) -> schema.ItemResult:
    item_record = db.query(models.Item).filter(models.Item.id == item_id).first()
    if not item_record:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_404_NOT_FOUND,
            detail=f"Bid at ID {item_id} not found",
        )

    return schema.ItemResult(**models.to_dict(item_record))


def create_item(data: schema.ItemCreateData, db: Session) -> schema.ItemResult:
    item_record = (
        db.query(models.Item)
        .filter(models.Item.composite_id == data.composite_id)
        .first()
    )
    if item_record:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_303_SEE_OTHER,
            detail=f"Item already exists at ID {item_record.id}",
        )

    item_model = models.Item(**data.dict())
    # Sync composite_id with current values
    setattr(item_model, "composite_id", data.composite_id)

    db.add(item_model)
    db.commit()

    return schema.ItemResult(**models.to_dict(item_model))


def update_item(
    item_id: int, data: schema.ItemUpdateData, db: Session
) -> schema.ItemResult:
    item_record = db.query(models.Item).filter(models.Item.id == item_id).first()
    if not item_record:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_404_NOT_FOUND,
            detail=f"Item at ID {item_id} not found",
        )

    for key, value in data.dict(exclude_none=True).items():
        setattr(item_record, key, value)

    # Sync composite_id with current values
    setattr(item_record, "composite_id", data.composite_id)

    db.add(item_record)
    db.commit()

    return schema.ItemResult(**models.to_dict(item_record))


def delete_item(item_id: int, db: Session) -> None:
    item_record = db.query(models.Item).filter(models.Item.id == item_id).first()
    if not item_record:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_404_NOT_FOUND,
            detail=f"Item at ID {item_id} not found",
        )

    db.delete(item_record)
    db.commit()
