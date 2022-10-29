import fastapi
from mndot_bid_api import operations
from mndot_bid_api.db import database
from mndot_bid_api.operations import enums, schema
from sqlalchemy.orm import Session

router = fastapi.APIRouter(prefix="/item", tags=["item"])


@router.get(
    "/{spec_year}/all",
    response_model=schema.ItemCollection,
    status_code=fastapi.status.HTTP_200_OK,
)
def api_read_all_items(
    spec_year: enums.SpecYear,
    db: Session = fastapi.Depends(database.get_db_session),
) -> schema.ItemCollection:

    return operations.items.read_all_items(spec_year, db)


@router.get(
    "/{spec_year}/{spec_code}/{unit_code}/{item_code}",
    response_model=schema.Item,
    status_code=fastapi.status.HTTP_200_OK,
)
def api_read_item(
    spec_year: enums.SpecYear,
    spec_code: str,
    unit_code: str,
    item_code: str,
    db: Session = fastapi.Depends(database.get_db_session),
) -> schema.Item:

    return operations.items.read_item(spec_year, spec_code, unit_code, item_code, db)


@router.get(
    "/{spec_year}/{search_string}",
    response_model=schema.ItemCollection,
    status_code=fastapi.status.HTTP_200_OK,
)
def api_search_item(
    spec_year: enums.SpecYear,
    search_string: str,
    db: Session = fastapi.Depends(database.get_db_session),
) -> schema.ItemCollection:

    return operations.items.search_item(spec_year, search_string, db)


@router.get(
    "/{item_id}",
    response_model=schema.Item,
    status_code=fastapi.status.HTTP_200_OK,
)
def api_read_item_by_id(
    item_id: int, db: Session = fastapi.Depends(database.get_db_session)
) -> schema.Item:

    return operations.items.read_item_by_id(item_id, db)


@router.post(
    "/",
    response_model=schema.Item,
    status_code=fastapi.status.HTTP_201_CREATED,
)
def api_create_item(
    data: schema.ItemCreateData, db: Session = fastapi.Depends(database.get_db_session)
) -> schema.Item:

    return operations.items.create_item(data, db)


@router.patch(
    "/{item_id}",
    response_model=schema.Item,
    status_code=fastapi.status.HTTP_200_OK,
)
def api_update_item(
    item_id: int,
    data: schema.ItemUpdateData,
    db: Session = fastapi.Depends(database.get_db_session),
) -> schema.Item:

    return operations.items.update_item(item_id, data, db)


@router.delete(
    "/{item_id}",
    status_code=fastapi.status.HTTP_204_NO_CONTENT,
)
def api_delete_item(
    item_id: int,
    db: Session = fastapi.Depends(database.get_db_session),
) -> None:

    return operations.items.delete_item(item_id, db)
