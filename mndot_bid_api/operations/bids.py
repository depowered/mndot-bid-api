from mndot_bid_api import exceptions, schema
from mndot_bid_api.operations.crud_interface import CRUDInterface


def read_all_bids(bid_interface: CRUDInterface) -> schema.BidCollection:
    records = bid_interface.read_all()
    results = [schema.BidResult(**record) for record in records]

    return schema.BidCollection(data=results)


def read_bid(bid_id: int, bid_interface: CRUDInterface) -> schema.Bid:
    try:
        record = bid_interface.read_by_id(bid_id)

    except exceptions.RecordNotFoundError as exc:
        exceptions.raise_http_404(model_name="Bid", id=bid_id, exc=exc)

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

    except exceptions.RecordNotFoundError as exc:
        raise exceptions.InvalidBidError(
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

    except exceptions.RecordAlreadyExistsError as exc:
        bid_id = exc.args[0]["id"]
        exceptions.raise_http_303(model_name="Bid", id=bid_id, exc=exc)

    result = schema.BidResult(**record)

    return schema.Bid(data=result)


def update_bid(
    bid_id: int, data: schema.BidUpdateData, bid_interface: CRUDInterface
) -> schema.Bid:
    try:
        record = bid_interface.update(id=bid_id, data=data.dict(exclude_none=True))

    except exceptions.RecordNotFoundError as exc:
        exceptions.raise_http_404(model_name="Bid", id=bid_id, exc=exc)

    result = schema.BidResult(**record)

    return schema.Bid(data=result)


def delete_bid(bid_id: int, bid_interface: CRUDInterface) -> None:
    try:
        bid_interface.delete(bid_id)

    except exceptions.RecordNotFoundError as exc:
        exceptions.raise_http_404(model_name="Bid", id=bid_id, exc=exc)


def query_bid(bid_interface: CRUDInterface, **kwargs) -> schema.BidCollection:

    if not kwargs:
        exceptions.raise_http_400_empty_query()

    try:
        records = bid_interface.read_all_by_kwargs(**kwargs)

    except exceptions.RecordNotFoundError as exc:
        exceptions.raise_http_404_query(model_name="Bid", exc=exc)

    results = [schema.BidResult(**record) for record in records]

    return schema.BidCollection(data=results)
