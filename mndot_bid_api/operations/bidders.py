import fastapi

from mndot_bid_api.exceptions import RecordAlreadyExistsError, RecordNotFoundError
from mndot_bid_api.operations import schema
from mndot_bid_api.operations.crud_interface import CRUDInterface


def read_all_bidders(bidder_interface: CRUDInterface) -> schema.BidderCollection:
    records = bidder_interface.read_all()
    results = [schema.BidderResult(**record) for record in records]

    return schema.BidderCollection(data=results)


def read_bidder(bidder_id: int, bidder_interface: CRUDInterface) -> schema.Bidder:
    try:
        record = bidder_interface.read_by_id(bidder_id)

    except RecordNotFoundError as exc:
        raise fastapi.HTTPException(
            status_code=404, detail=f"Bidder at ID {bidder_id} not found."
        ) from exc

    result = schema.BidderResult(**record)

    return schema.Bidder(data=result)


def create_bidder(
    data: schema.BidderCreateData, bidder_interface: CRUDInterface
) -> schema.Bidder:
    try:
        record = bidder_interface.create(data.dict())

    except RecordAlreadyExistsError as exc:
        raise fastapi.HTTPException(
            status_code=303, detail=f"Bidder already exists at ID {data.id}"
        ) from exc

    result = schema.BidderResult(**record)

    return schema.Bidder(data=result)


def update_bidder(
    bidder_id: int, data: schema.BidderUpdateData, bidder_interface: CRUDInterface
) -> schema.Bidder:
    try:
        record = bidder_interface.update(
            id=bidder_id, data=data.dict(exclude_none=True)
        )

    except RecordNotFoundError as exc:
        raise fastapi.HTTPException(
            status_code=404, detail=f"Bidder at ID {bidder_id} not found."
        ) from exc

    result = schema.BidderResult(**record)

    return schema.Bidder(data=result)


def delete_bidder(bidder_id: int, bidder_interface: CRUDInterface) -> None:
    try:
        bidder_interface.delete(bidder_id)

    except RecordNotFoundError as exc:
        raise fastapi.HTTPException(
            status_code=404, detail=f"Bidder at ID {bidder_id} not found."
        ) from exc


def query_bidder(bidder_interface: CRUDInterface, **kwargs) -> schema.BidderCollection:
    if not kwargs:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_400_BAD_REQUEST,
            detail=f"Provide at least one query parameter",
        )

    try:
        records = bidder_interface.read_all_by_kwargs(**kwargs)

    except RecordNotFoundError as exc:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_404_NOT_FOUND,
            detail=f"No Bidders found matching the provided query parameters",
        ) from exc

    results = [schema.BidderResult(**record) for record in records]

    return schema.BidderCollection(data=results)
