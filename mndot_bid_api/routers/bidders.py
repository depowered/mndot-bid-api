import fastapi
from mndot_bid_api import operations
from mndot_bid_api.db import database
from mndot_bid_api.operations import schema
from sqlalchemy.orm import Session

router = fastapi.APIRouter(prefix="/bidder", tags=["bidder"])


@router.get(
    "/all",
    response_model=schema.BidderCollection,
    status_code=fastapi.status.HTTP_200_OK,
)
def api_read_all_bidders(
    db: Session = fastapi.Depends(database.get_db_session),
) -> schema.BidderCollection:

    return operations.bidders.read_all_bidders(db)


@router.get(
    "/{bidder_id}",
    response_model=schema.Bidder,
    status_code=fastapi.status.HTTP_200_OK,
)
def api_read_bidder(
    bidder_id: int, db: Session = fastapi.Depends(database.get_db_session)
) -> schema.Bidder:

    return operations.bidders.read_bidder(bidder_id, db)


@router.post(
    "/",
    response_model=schema.Bidder,
    status_code=fastapi.status.HTTP_200_OK,
)
def api_create_bidder(
    data: schema.BidderCreateData,
    db: Session = fastapi.Depends(database.get_db_session),
) -> schema.Bidder:

    return operations.bidders.create_bidder(data, db)


@router.patch(
    "/{bidder_id}",
    response_model=schema.Bidder,
    status_code=fastapi.status.HTTP_200_OK,
)
def api_update_bidder(
    bidder_id: int,
    data: schema.BidderUpdateData,
    db: Session = fastapi.Depends(database.get_db_session),
) -> schema.Bidder:

    return operations.bidders.update_bidder(bidder_id, data, db)


@router.delete(
    "/{bidder_id}",
    status_code=fastapi.status.HTTP_204_NO_CONTENT,
)
def api_delete_bidder(
    bidder_id: int,
    db: Session = fastapi.Depends(database.get_db_session),
):

    return operations.bidders.delete_bidder(bidder_id, db)
