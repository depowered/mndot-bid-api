import fastapi
from mndot_bid_api.db import database
from mndot_bid_api.operations import items, schema
from sqlalchemy.orm import Session

router = fastapi.APIRouter()


@router.get(
    "/item/all",
    tags=["item"],
    response_model=list[schema.ItemResult],
    status_code=fastapi.status.HTTP_200_OK,
)
def api_read_all_items(
    db: Session = fastapi.Depends(database.get_db_session),
) -> schema.ItemResult:
    return items.read_all_items(db)


@router.get(
    "/item/{item_id}",
    tags=["item"],
    response_model=schema.ItemResult,
    status_code=fastapi.status.HTTP_200_OK,
)
def api_read_item(
    item_id: int, db: Session = fastapi.Depends(database.get_db_session)
) -> schema.ItemResult:
    return items.read_item(item_id, db)


@router.post(
    "/item",
    tags=["item"],
    response_model=schema.ItemResult,
    status_code=fastapi.status.HTTP_201_CREATED,
)
def api_create_item(
    data: schema.ItemCreateData, db: Session = fastapi.Depends(database.get_db_session)
) -> schema.ItemResult:
    return items.create_item(data, db)


@router.patch(
    "/item/{item_id}",
    tags=["item"],
    response_model=schema.ItemResult,
    status_code=fastapi.status.HTTP_200_OK,
)
def api_update_item(
    item_id: int,
    data: schema.ItemUpdateData,
    db: Session = fastapi.Depends(database.get_db_session),
) -> schema.ItemResult:
    return items.update_item(item_id, data, db)


@router.delete(
    "/item/{item_id}",
    tags=["item"],
    status_code=fastapi.status.HTTP_204_NO_CONTENT,
)
def api_delete_item(
    item_id: int,
    db: Session = fastapi.Depends(database.get_db_session),
):
    return items.delete_item(item_id, db)
