import fastapi
from mndot_bid_api.db import models
from mndot_bid_api.operations import enums, schema
from sqlalchemy.orm import Session


class InvalidBidExecption(Exception):
    pass


def read_all_bids(db: Session) -> schema.BidCollection:

    bid_records = db.query(models.Bid).all()

    bid_results = [schema.BidResult(**models.to_dict(bid)) for bid in bid_records]

    return schema.BidCollection(data=bid_results)


def read_bid(bid_id: int, db: Session) -> schema.Bid:

    bid_record = db.query(models.Bid).filter(models.Bid.id == bid_id).first()

    if not bid_record:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_404_NOT_FOUND,
            detail=f"Bid at ID {bid_id} not found",
        )

    return schema.Bid(data=schema.BidResult(**models.to_dict(bid_record)))


def create_bid(data: schema.BidCreateData, db: Session) -> schema.Bid:
    # Get matching item record so that item_id can be assigned to the new bid record
    item_record = (
        db.query(models.Item)
        .filter(
            models.Item.spec_code == data.item_spec_code,
            models.Item.unit_code == data.item_unit_code,
            models.Item.item_code == data.item_item_code,
            models.Item.long_description == data.item_long_description,
            models.Item.unit_abbreviation == data.item_unit_abbreviation,
        )
        .first()
    )

    if not item_record:
        raise InvalidBidExecption(
            "No matching item found. Redirect to create invalid bid."
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

    return schema.Bid(data=schema.BidResult(**models.to_dict(bid_model)))


def update_bid(bid_id: int, data: schema.BidUpdateData, db: Session) -> schema.Bid:

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

    return schema.Bid(data=schema.BidResult(**models.to_dict(bid_record)))


def delete_bid(bid_id: int, db: Session) -> None:

    bid_record = db.query(models.Bid).filter(models.Bid.id == bid_id).first()

    if not bid_record:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_404_NOT_FOUND,
            detail=f"Bid at ID {bid_id} not found",
        )

    db.delete(bid_record)
    db.commit()


def query_bid(
    contract_id: int | None,
    item_id: int | None,
    bidder_id: int | None,
    bid_type: enums.BidType | None,
    db: Session,
) -> schema.BidCollection:

    # build a dyanmic query dictionary and pass to the filter_by function
    filter_kwargs = {}
    if contract_id:
        filter_kwargs["contract_id"] = contract_id
    if item_id:
        filter_kwargs["item_id"] = item_id
    if bidder_id:
        filter_kwargs["bidder_id"] = bidder_id
    if bid_type:
        filter_kwargs["bid_type"] = bid_type

    if not filter_kwargs:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_400_BAD_REQUEST,
            detail=f"Provide at least one query parameter",
        )

    bid_records = db.query(models.Bid).filter_by(**filter_kwargs).all()

    if not bid_records:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_404_NOT_FOUND,
            detail=f"No Bids found matching the provided query parameters",
        )

    bid_results = [schema.BidResult(**models.to_dict(bid)) for bid in bid_records]

    return schema.BidCollection(data=bid_results)
