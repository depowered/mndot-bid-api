from mndot_bid_api import exceptions, schema
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

    except exceptions.RecordNotFoundError as exc:
        exceptions.raise_http_404(model_name="Invalid Bid", id=invalid_bid_id, exc=exc)

    result = schema.InvalidBidResult(**record)

    return schema.InvalidBid(data=result)


def create_invalid_bid(
    data: schema.BidCreateData, invalid_bid_interface: CRUDInterface
) -> schema.InvalidBid:
    try:
        record = invalid_bid_interface.create(data.dict())

    except exceptions.RecordAlreadyExistsError as exc:
        invalid_bid_id = exc.args[0]["id"]
        exceptions.raise_http_303(model_name="Invalid Bid", id=invalid_bid_id, exc=exc)

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

    except exceptions.RecordNotFoundError as exc:
        exceptions.raise_http_404(model_name="Invalid Bid", id=invalid_bid_id, exc=exc)

    result = schema.InvalidBidResult(**record)

    return schema.InvalidBid(data=result)


def delete_invalid_bid(
    invalid_bid_id: int, invalid_bid_interface: CRUDInterface
) -> None:
    try:
        invalid_bid_interface.delete(invalid_bid_id)

    except exceptions.RecordNotFoundError as exc:
        exceptions.raise_http_404(model_name="Invalid Bid", id=invalid_bid_id, exc=exc)


def query_invalid_bid(
    invalid_bid_interface: CRUDInterface, **kwargs
) -> schema.InvalidBidCollection:
    if not kwargs:
        exceptions.raise_http_400_empty_query()

    try:
        records = invalid_bid_interface.read_all_by_kwargs(**kwargs)

    except exceptions.RecordNotFoundError as exc:
        exceptions.raise_http_404_query(model_name="Invalid Bid", exc=exc)

    results = [schema.InvalidBidResult(**record) for record in records]

    return schema.InvalidBidCollection(data=results)
