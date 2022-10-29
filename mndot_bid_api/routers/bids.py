import fastapi
from mndot_bid_api import operations
from mndot_bid_api.db import database
from mndot_bid_api.operations import enums, schema
from sqlalchemy.orm import Session

router = fastapi.APIRouter(prefix="/bid")


@router.get(
    "/all",
    tags=["bid"],
    response_model=schema.BidCollection,
    status_code=fastapi.status.HTTP_200_OK,
)
def api_read_all_bids(
    db: Session = fastapi.Depends(database.get_db_session),
) -> schema.BidCollection:

    return operations.bids.read_all_bids(db)


@router.get(
    "/{bid_id}",
    tags=["bid"],
    response_model=schema.Bid,
    status_code=fastapi.status.HTTP_200_OK,
)
def api_read_bid(
    bid_id: int, db: Session = fastapi.Depends(database.get_db_session)
) -> schema.Bid:

    return operations.bids.read_bid(bid_id, db)


@router.post(
    "/",
    tags=["bid"],
    response_model=schema.Bid,
    status_code=fastapi.status.HTTP_201_CREATED,
)
def api_create_bid(
    data: schema.BidCreateData, db: Session = fastapi.Depends(database.get_db_session)
) -> schema.Bid | fastapi.responses.RedirectResponse:

    try:
        bid_result = operations.bids.create_bid(data, db)
        return bid_result

    except operations.bids.InvalidBidExecption:
        return fastapi.responses.RedirectResponse(
            "/invalid_bid/",
            status_code=fastapi.status.HTTP_307_TEMPORARY_REDIRECT,
        )


@router.patch(
    "/{bid_id}",
    tags=["bid"],
    response_model=schema.Bid,
    status_code=fastapi.status.HTTP_200_OK,
)
def api_update_bid(
    bid_id: int,
    data: schema.BidUpdateData,
    db: Session = fastapi.Depends(database.get_db_session),
) -> schema.Bid:

    return operations.bids.update_bid(bid_id, data, db)


@router.delete(
    "/{bid_id}",
    tags=["bid"],
    status_code=fastapi.status.HTTP_204_NO_CONTENT,
)
def api_delete_bid(
    bid_id: int,
    db: Session = fastapi.Depends(database.get_db_session),
):

    return operations.bids.delete_bid(bid_id, db)


@router.get(
    "/query/",
    tags=["bid"],
    response_model=schema.BidCollection,
    status_code=fastapi.status.HTTP_200_OK,
)
def api_query_bid(
    contract_id: int | None = None,
    item_id: int | None = None,
    bidder_id: int | None = None,
    bid_type: enums.BidType | None = None,
    db: Session = fastapi.Depends(database.get_db_session),
) -> schema.BidCollection:

    return operations.bids.query_bid(contract_id, item_id, bidder_id, bid_type, db)
