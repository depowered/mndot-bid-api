from mndot_bid_api import exceptions, schema
from mndot_bid_api.operations.crud_interface import CRUDInterface


def read_all_bidders(bidder_interface: CRUDInterface) -> schema.BidderCollection:
    records = bidder_interface.read_all()
    results = [schema.BidderResult(**record) for record in records]

    return schema.BidderCollection(data=results)


def read_bidder(bidder_id: int, bidder_interface: CRUDInterface) -> schema.Bidder:
    try:
        record = bidder_interface.read_by_id(bidder_id)

    except exceptions.RecordNotFoundError as exc:
        exceptions.raise_http_404(model_name="Bidder", id=bidder_id, exc=exc)

    result = schema.BidderResult(**record)

    return schema.Bidder(data=result)


def create_bidder(
    data: schema.BidderCreateData, bidder_interface: CRUDInterface
) -> schema.Bidder:
    try:
        record = bidder_interface.create(data.dict())

    except exceptions.RecordAlreadyExistsError as exc:
        bidder_id = exc.args[0]["id"]
        exceptions.raise_http_303(model_name="Bidder", id=bidder_id, exc=exc)

    result = schema.BidderResult(**record)

    return schema.Bidder(data=result)


def update_bidder(
    bidder_id: int, data: schema.BidderUpdateData, bidder_interface: CRUDInterface
) -> schema.Bidder:
    try:
        record = bidder_interface.update(
            id=bidder_id, data=data.dict(exclude_none=True)
        )

    except exceptions.RecordNotFoundError as exc:
        exceptions.raise_http_404(model_name="Bidder", id=bidder_id, exc=exc)

    result = schema.BidderResult(**record)

    return schema.Bidder(data=result)


def delete_bidder(bidder_id: int, bidder_interface: CRUDInterface) -> None:
    try:
        bidder_interface.delete(bidder_id)

    except exceptions.RecordNotFoundError as exc:
        exceptions.raise_http_404(model_name="Bidder", id=bidder_id, exc=exc)


def query_bidder(bidder_interface: CRUDInterface, **kwargs) -> schema.BidderCollection:
    if not kwargs:
        exceptions.raise_http_400_empty_query()

    try:
        records = bidder_interface.read_all_by_kwargs(**kwargs)

    except exceptions.RecordNotFoundError as exc:
        exceptions.raise_http_404_query(model_name="Bidder", exc=exc)

    results = [schema.BidderResult(**record) for record in records]

    return schema.BidderCollection(data=results)
