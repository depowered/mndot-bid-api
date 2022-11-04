import fastapi
from mndot_bid_api import db, operations
from mndot_bid_api.exceptions import RecordAlreadyExistsException
from mndot_bid_api.operations import schema

router = fastapi.APIRouter(prefix="/item", tags=["item"])


@router.get(
    "/all",
    response_model=schema.ItemCollection,
    status_code=fastapi.status.HTTP_200_OK,
)
def api_read_all_items(
    item_interface=fastapi.Depends(db.get_item_interface),
) -> schema.ItemCollection:

    return operations.items.read_all_items(item_interface)


@router.get(
    "/{item_id}",
    response_model=schema.Item,
    status_code=fastapi.status.HTTP_200_OK,
)
def api_read_item_by_id(
    item_id: int, item_interface=fastapi.Depends(db.get_item_interface)
) -> schema.Item:

    return operations.items.read_item_by_id(item_id, item_interface)


@router.post(
    "/",
    response_model=schema.Item,
    status_code=fastapi.status.HTTP_201_CREATED,
)
def api_create_item(
    data: schema.ItemCreateData, item_interface=fastapi.Depends(db.get_item_interface)
) -> schema.Item:

    try:
        item_result = operations.items.create_item(data, item_interface)
        return item_result

    except RecordAlreadyExistsException as exc:
        item_id = exc.args[0]["id"]
        update_data = schema.ItemUpdateData(**data.dict(exclude_none=True))
        return operations.items.update_item(item_id, update_data, item_interface)


@router.patch(
    "/{item_id}",
    response_model=schema.Item,
    status_code=fastapi.status.HTTP_200_OK,
)
def api_update_item(
    item_id: int,
    data: schema.ItemUpdateData,
    item_interface=fastapi.Depends(db.get_item_interface),
) -> schema.Item:

    return operations.items.update_item(item_id, data, item_interface)


@router.delete(
    "/{item_id}",
    status_code=fastapi.status.HTTP_204_NO_CONTENT,
)
def api_delete_item(
    item_id: int,
    item_interface=fastapi.Depends(db.get_item_interface),
) -> None:

    return operations.items.delete_item(item_id, item_interface)


@router.get(
    "/query/",
    response_model=schema.ItemCollection,
    status_code=fastapi.status.HTTP_200_OK,
)
def api_query_item(
    item_interface=fastapi.Depends(db.get_item_interface),
    spec_code: str | None = None,
    unit_code: str | None = None,
    item_code: str | None = None,
    short_description: str | None = None,
    long_description: str | None = None,
    unit: str | None = None,
    unit_abbreviation: str | None = None,
    in_spec_2016: bool | None = None,
    in_spec_2018: bool | None = None,
    in_spec_2020: bool | None = None,
    in_spec_2022: bool | None = None,
) -> schema.ItemCollection:
    kwargs = locals()

    # Filter for non-None keyword arguments to pass to the query function
    filtered_kwargs = {
        key: value for key, value in kwargs.items() if value and key != "item_interface"
    }

    return operations.items.query_item(item_interface, **filtered_kwargs)
