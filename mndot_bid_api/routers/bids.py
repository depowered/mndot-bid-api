import fastapi
from mndot_bid_api import operations
from mndot_bid_api.db import database
from mndot_bid_api.operations import enums, schema
from sqlalchemy.orm import Session

router = fastapi.APIRouter()


@router.get(
    "/bid/all",
    tags=["bid"],
    response_model=list[schema.BidResult],
    status_code=fastapi.status.HTTP_200_OK,
)
def api_read_all_bids(
    db: Session = fastapi.Depends(database.get_db_session),
) -> schema.BidResult:

    return operations.bids.read_all_bids(db)


@router.get(
    "/bid/{bid_id}",
    tags=["bid"],
    response_model=schema.BidResult,
    status_code=fastapi.status.HTTP_200_OK,
)
def api_read_bid(
    bid_id: int, db: Session = fastapi.Depends(database.get_db_session)
) -> schema.BidResult:

    return operations.bids.read_bid(bid_id, db)


@router.post(
    "/bid",
    tags=["bid"],
    response_model=schema.BidResult,
    status_code=fastapi.status.HTTP_201_CREATED,
)
def api_create_bid(
    data: schema.BidCreateData, db: Session = fastapi.Depends(database.get_db_session)
) -> schema.BidResult:

    return operations.bids.create_bid(data, db)


@router.patch(
    "/bid/{bid_id}",
    tags=["bid"],
    response_model=schema.BidResult,
    status_code=fastapi.status.HTTP_200_OK,
)
def api_update_bid(
    bid_id: int,
    data: schema.BidUpdateData,
    db: Session = fastapi.Depends(database.get_db_session),
) -> schema.BidResult:

    return operations.bids.update_bid(bid_id, data, db)


@router.delete(
    "/bid/{bid_id}",
    tags=["bid"],
    status_code=fastapi.status.HTTP_204_NO_CONTENT,
)
def api_delete_bid(
    bid_id: int,
    db: Session = fastapi.Depends(database.get_db_session),
):

    return operations.bids.delete_bid(bid_id, db)


@router.get(
    "/bid/query/",
    tags=["bid"],
    response_model=list[schema.BidResult],
    status_code=fastapi.status.HTTP_200_OK,
)
def api_query_bid(
    contract_id: int | None = None,
    item_id: int | None = None,
    bidder_id: int | None = None,
    bid_type: enums.BidType | None = None,
    db: Session = fastapi.Depends(database.get_db_session),
) -> list[schema.BidResult]:

    return operations.bids.query_bid(contract_id, item_id, bidder_id, bid_type, db)
