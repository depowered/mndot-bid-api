import fastapi

from mndot_bid_api.exceptions import (
    InvalidBidError,
    RecordAlreadyExistsError,
    RecordNotFoundError,
)
from mndot_bid_api.operations import schema
from mndot_bid_api.operations.crud_interface import CRUDInterface


def read_all_bids(bid_interface: CRUDInterface) -> schema.BidCollection:
    records = bid_interface.read_all()
    results = [schema.BidResult(**record) for record in records]

    return schema.BidCollection(data=results)


def read_bid(bid_id: int, bid_interface: CRUDInterface) -> schema.Bid:
    try:
        record = bid_interface.read_by_id(bid_id)

    except RecordNotFoundError as exc:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_404_NOT_FOUND,
            detail=f"Bid at ID {bid_id} not found",
        ) from exc

    result = schema.BidResult(**record)

    return schema.Bid(data=result)


def create_bid(
    data: schema.BidCreateData,
    bid_interface: CRUDInterface,
    item_interface: CRUDInterface,
) -> schema.Bid:
    # Get matching item record so that item_id can be assigned to the new bid record
    item_filter_kwargs = {
        "spec_code": data.item_spec_code,
        "unit_code": data.item_unit_code,
        "item_code": data.item_item_code,
        "long_description": data.item_long_description,
        "unit_abbreviation": data.item_unit_abbreviation,
    }
    try:
        item_record = item_interface.read_one_by_kwargs(**item_filter_kwargs)

    except RecordNotFoundError as exc:
        raise InvalidBidError(
            "No matching item found. Redirect to create invalid bid."
        ) from exc

    # Prepare a bid record dictionary from the BidCreateData object that:
    #   Excludes all fields that begin with "item_"
    #   Includes "item_id" matching item_record.id
    bid_record_dict = data.dict(
        exclude={field for field in data.__fields_set__ if "item_" in field}
    )
    bid_record_dict.update({"item_id": item_record["id"]})

    try:
        record = bid_interface.create(bid_record_dict)

    except RecordAlreadyExistsError as exc:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_303_SEE_OTHER,
            detail=f"Bid already exists at ID {exc.args[0]['id']}",
        ) from exc

    result = schema.BidResult(**record)

    return schema.Bid(data=result)


def update_bid(
    bid_id: int, data: schema.BidUpdateData, bid_interface: CRUDInterface
) -> schema.Bid:
    try:
        record = bid_interface.update(id=bid_id, data=data.dict(exclude_none=True))

    except RecordNotFoundError as exc:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_404_NOT_FOUND,
            detail=f"Bid at ID {bid_id} not found",
        ) from exc

    result = schema.BidResult(**record)

    return schema.Bid(data=result)


def delete_bid(bid_id: int, bid_interface: CRUDInterface) -> None:
    try:
        bid_interface.delete(bid_id)

    except RecordNotFoundError as exc:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_404_NOT_FOUND,
            detail=f"Bid at ID {bid_id} not found",
        ) from exc


def query_bid(bid_interface: CRUDInterface, **kwargs) -> schema.BidCollection:

    if not kwargs:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_400_BAD_REQUEST,
            detail=f"Provide at least one query parameter",
        )

    try:
        records = bid_interface.read_all_by_kwargs(**kwargs)

    except RecordNotFoundError as exc:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_404_NOT_FOUND,
            detail=f"No Bids found matching the provided query parameters",
        ) from exc

    results = [schema.BidResult(**record) for record in records]

    return schema.BidCollection(data=results)
