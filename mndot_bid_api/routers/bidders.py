import fastapi
from mndot_bid_api.db import database
from mndot_bid_api.operations import bidders, schema
from sqlalchemy.orm import Session

router = fastapi.APIRouter()


@router.get(
    "/bidder/all",
    tags=["bidder"],
    response_model=list[schema.BidderResult],
    status_code=fastapi.status.HTTP_200_OK,
)
def api_read_all_bidders(
    db: Session = fastapi.Depends(database.get_db_session),
) -> list[schema.BidderResult]:
    return bidders.read_all_bidders(db)


@router.get(
    "/bidder/{bidder_id}",
    tags=["bidder"],
    response_model=schema.BidderResult,
    status_code=fastapi.status.HTTP_200_OK,
)
def api_read_bidder(
    bidder_id: int, db: Session = fastapi.Depends(database.get_db_session)
) -> schema.BidderResult:
    return bidders.read_bidder(bidder_id, db)


@router.post(
    "/bidder",
    tags=["bidder"],
    response_model=schema.BidderResult,
    status_code=fastapi.status.HTTP_200_OK,
)
def api_create_bidder(
    data: schema.BidderCreateData,
    db: Session = fastapi.Depends(database.get_db_session),
) -> schema.BidderResult:
    return bidders.create_bidder(data, db)


@router.patch(
    "/bidder/{bidder_id}",
    tags=["bidder"],
    response_model=schema.BidderResult,
    status_code=fastapi.status.HTTP_200_OK,
)
def api_update_bidder(
    bidder_id: int,
    data: schema.BidderUpdateData,
    db: Session = fastapi.Depends(database.get_db_session),
) -> schema.BidderResult:
    return bidders.update_bidder(bidder_id, data, db)


@router.delete(
    "/bidder/{bidder_id}",
    tags=["bidder"],
    status_code=fastapi.status.HTTP_204_NO_CONTENT,
)
def api_delete_bidder(
    bidder_id: int,
    db: Session = fastapi.Depends(database.get_db_session),
):
    return bidders.delete_bidder(bidder_id, db)
