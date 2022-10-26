import fastapi
from mndot_bid_api import operations
from mndot_bid_api.db import database
from mndot_bid_api.operations import schema
from sqlalchemy.orm import Session

router = fastapi.APIRouter(prefix="/invalid_bid")


@router.get(
    "/all",
    tags=["invalid_bid"],
    response_model=list[schema.InvalidBidResult],
    status_code=fastapi.status.HTTP_200_OK,
)
def api_read_all_invalid_bids(
    db: Session = fastapi.Depends(database.get_db_session),
) -> list[schema.InvalidBidResult]:

    return operations.invalid_bids.read_all_invalid_bids(db)


@router.get(
    "/{invalid_bid_id}",
    tags=["invalid_bid"],
    response_model=schema.InvalidBidResult,
    status_code=fastapi.status.HTTP_200_OK,
)
def api_read_invalid_bid_by_id(
    invalid_bid_id: int,
    db: Session = fastapi.Depends(database.get_db_session),
) -> schema.InvalidBidResult:

    return operations.invalid_bids.read_invalid_bid_by_id(invalid_bid_id, db)


@router.post(
    "/",
    tags=["invalid_bid"],
    response_model=schema.InvalidBidResult,
    status_code=fastapi.status.HTTP_201_CREATED,
)
def api_create_invalid_bid(
    data: schema.InvalidBidCreateData,
    db: Session = fastapi.Depends(database.get_db_session),
) -> schema.InvalidBidResult:

    return operations.invalid_bids.create_invalid_bid(data, db)


@router.patch(
    "/{invalid_bid_id}",
    tags=["invalid_bid"],
    response_model=schema.InvalidBidResult,
    status_code=fastapi.status.HTTP_200_OK,
)
def api_update_invalid_bid(
    invalid_bid_id: int,
    data: schema.InvalidBidUpdateData,
    db: Session = fastapi.Depends(database.get_db_session),
) -> schema.InvalidBidResult:

    return operations.invalid_bids.update_invalid_bid(invalid_bid_id, data, db)


@router.delete(
    "/{invalid_bid_id}",
    tags=["invalid_bid"],
    status_code=fastapi.status.HTTP_204_NO_CONTENT,
)
def api_delete_invalid_bid(
    invalid_bid_id: int,
    db: Session = fastapi.Depends(database.get_db_session),
) -> None:

    return operations.invalid_bids.delete_invalid_bid(invalid_bid_id, db)
