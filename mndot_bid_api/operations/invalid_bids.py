import fastapi
from mndot_bid_api.exceptions import (
    RecordAlreadyExistsException,
    RecordNotFoundException,
)
from mndot_bid_api.operations import schema
from mndot_bid_api.operations.crud_interface import CRUDInterface


def read_all_invalid_bids(
    invalid_bid_interface: CRUDInterface,
) -> schema.InvalidBidCollection:
    records = invalid_bid_interface.read_all()
    results = [schema.InvalidBidResult(**record) for record in records]

    return schema.InvalidBidCollection(data=results)


def read_invalid_bid_by_id(
    invalid_bid_id: int, invalid_bid_interface: CRUDInterface
) -> schema.InvalidBid:
    try:
        record = invalid_bid_interface.read_by_id(invalid_bid_id)

    except RecordNotFoundException as exc:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_404_NOT_FOUND,
            detail=f"Invalid bid record at ID {invalid_bid_id} not found",
        ) from exc

    result = schema.InvalidBidResult(**record)

    return schema.InvalidBid(data=result)


def create_invalid_bid(
    data: schema.BidCreateData, invalid_bid_interface: CRUDInterface
) -> schema.InvalidBid:
    try:
        record = invalid_bid_interface.create(data.dict())

    except RecordAlreadyExistsException as exc:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_303_SEE_OTHER,
            detail=f"Invalid bid record already exists at ID {exc.args[0]['id']}",
        ) from exc

    result = schema.InvalidBidResult(**record)

    return schema.InvalidBid(data=result)


def update_invalid_bid(
    invalid_bid_id: int,
    data: schema.InvalidBidUpdateData,
    invalid_bid_interface: CRUDInterface,
) -> schema.InvalidBid:
    try:
        record = invalid_bid_interface.update(
            invalid_bid_id, data.dict(exclude_none=True)
        )

    except RecordNotFoundException as exc:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_404_NOT_FOUND,
            detail=f"Invalid bid record at ID {invalid_bid_id} not found",
        ) from exc

    result = schema.InvalidBidResult(**record)

    return schema.InvalidBid(data=result)


def delete_invalid_bid(
    invalid_bid_id: int, invalid_bid_interface: CRUDInterface
) -> None:
    try:
        invalid_bid_interface.delete(invalid_bid_id)

    except RecordNotFoundException as exc:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_404_NOT_FOUND,
            detail=f"Invalid bid record at ID {invalid_bid_id} not found",
        ) from exc


def query_invalid_bid(
    invalid_bid_interface: CRUDInterface, **kwargs
) -> schema.InvalidBidCollection:
    if not kwargs:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_400_BAD_REQUEST,
            detail=f"Provide at least one query parameter",
        )

    try:
        records = invalid_bid_interface.read_all_by_kwargs(**kwargs)

    except RecordNotFoundException as exc:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_404_NOT_FOUND,
            detail=f"No Invalid Bids found matching the provided query parameters",
        ) from exc

    results = [schema.InvalidBidResult(**record) for record in records]

    return schema.InvalidBidCollection(data=results)
