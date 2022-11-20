from mndot_bid_api import exceptions, schema
from mndot_bid_api.operations.crud_interface import CRUDInterface


def read_all_items(item_interface: CRUDInterface) -> schema.ItemCollection:
    records = item_interface.read_all()
    results = [schema.ItemResult(**record) for record in records]

    return schema.ItemCollection(data=results)


def read_item_by_id(item_id: int, item_interface: CRUDInterface) -> schema.Item:
    try:
        record = item_interface.read_by_id(item_id)

    except exceptions.RecordNotFoundError as exc:
        exceptions.raise_http_404(model_name="Item", id=item_id, exc=exc)

    result = schema.ItemResult(**record)

    return schema.Item(data=result)


def create_item(
    data: schema.ItemCreateData, item_interface: CRUDInterface
) -> schema.Item:
    try:
        record = item_interface.create(data.dict(exclude_none=True))

    except exceptions.RecordAlreadyExistsError as exc:
        item_id = exc.args[0]["id"]
        exceptions.raise_http_303(model_name="Item", id=item_id, exc=exc)

    result = schema.ItemResult(**record)

    return schema.Item(data=result)


def update_item(
    item_id: int, data: schema.ItemUpdateData, item_interface: CRUDInterface
) -> schema.Item:
    try:
        record = item_interface.update(item_id, data=data.dict(exclude_none=True))

    except exceptions.RecordNotFoundError as exc:
        exceptions.raise_http_404(model_name="Item", id=item_id, exc=exc)

    result = schema.ItemResult(**record)

    return schema.Item(data=result)


def delete_item(item_id: int, item_interface: CRUDInterface) -> None:
    try:
        item_interface.delete(item_id)

    except exceptions.RecordNotFoundError as exc:
        exceptions.raise_http_404(model_name="Item", id=item_id, exc=exc)


def query_item(item_interface: CRUDInterface, **kwargs) -> schema.ItemCollection:
    if not kwargs:
        exceptions.raise_http_400_empty_query()

    try:
        records = item_interface.read_all_by_kwargs(**kwargs)

    except exceptions.RecordNotFoundError as exc:
        exceptions.raise_http_404_query(model_name="Item", exc=exc)

    results = [schema.ItemResult(**record) for record in records]

    return schema.ItemCollection(data=results)
