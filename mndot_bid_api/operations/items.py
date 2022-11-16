import fastapi

from mndot_bid_api.exceptions import RecordAlreadyExistsException, RecordNotFoundError
from mndot_bid_api.operations import schema
from mndot_bid_api.operations.crud_interface import CRUDInterface


def read_all_items(item_interface: CRUDInterface) -> schema.ItemCollection:
    records = item_interface.read_all()
    results = [schema.ItemResult(**record) for record in records]

    return schema.ItemCollection(data=results)


def read_item_by_id(item_id: int, item_interface: CRUDInterface) -> schema.Item:
    try:
        record = item_interface.read_by_id(item_id)

    except RecordNotFoundError as exc:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_404_NOT_FOUND,
            detail=f"Item at ID {item_id} not found",
        ) from exc

    result = schema.ItemResult(**record)

    return schema.Item(data=result)


def create_item(
    data: schema.ItemCreateData, item_interface: CRUDInterface
) -> schema.Item:
    try:
        record = item_interface.create(data.dict(exclude_none=True))

    except RecordAlreadyExistsException as exc:
        raise exc

    result = schema.ItemResult(**record)

    return schema.Item(data=result)


def update_item(
    item_id: int, data: schema.ItemUpdateData, item_interface: CRUDInterface
) -> schema.Item:
    try:
        record = item_interface.update(item_id, data=data.dict(exclude_none=True))

    except RecordNotFoundError as exc:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_404_NOT_FOUND,
            detail=f"Item at ID {item_id} not found",
        ) from exc

    result = schema.ItemResult(**record)

    return schema.Item(data=result)


def delete_item(item_id: int, item_interface: CRUDInterface) -> None:
    try:
        item_interface.delete(item_id)

    except RecordNotFoundError as exc:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_404_NOT_FOUND,
            detail=f"Item at ID {item_id} not found",
        ) from exc


def query_item(item_interface: CRUDInterface, **kwargs) -> schema.ItemCollection:
    if not kwargs:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_400_BAD_REQUEST,
            detail=f"Provide at least one query parameter",
        )

    try:
        records = item_interface.read_all_by_kwargs(**kwargs)

    except RecordNotFoundError as exc:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_404_NOT_FOUND,
            detail=f"No Items found matching the provided query parameters",
        ) from exc

    results = [schema.ItemResult(**record) for record in records]

    return schema.ItemCollection(data=results)
