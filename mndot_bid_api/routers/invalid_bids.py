import fastapi
from mndot_bid_api import db, operations
from mndot_bid_api.operations import schema

router = fastapi.APIRouter(prefix="/invalid_bid", tags=["invalid_bid"])


@router.get(
    "/all",
    response_model=schema.InvalidBidCollection,
    status_code=fastapi.status.HTTP_200_OK,
)
def api_read_all_invalid_bids(
    invalid_bid_interface=fastapi.Depends(db.get_invalid_bid_interface),
) -> schema.InvalidBidCollection:

    return operations.invalid_bids.read_all_invalid_bids(invalid_bid_interface)


@router.get(
    "/{invalid_bid_id}",
    response_model=schema.InvalidBid,
    status_code=fastapi.status.HTTP_200_OK,
)
def api_read_invalid_bid_by_id(
    invalid_bid_id: int,
    invalid_bid_interface=fastapi.Depends(db.get_invalid_bid_interface),
) -> schema.InvalidBid:

    return operations.invalid_bids.read_invalid_bid_by_id(
        invalid_bid_id, invalid_bid_interface
    )


@router.post(
    "/",
    response_model=schema.InvalidBid,
    status_code=fastapi.status.HTTP_201_CREATED,
)
def api_create_invalid_bid(
    data: schema.BidCreateData,
    invalid_bid_interface=fastapi.Depends(db.get_invalid_bid_interface),
) -> schema.InvalidBid:

    return operations.invalid_bids.create_invalid_bid(data, invalid_bid_interface)


@router.patch(
    "/{invalid_bid_id}",
    response_model=schema.InvalidBid,
    status_code=fastapi.status.HTTP_200_OK,
)
def api_update_invalid_bid(
    invalid_bid_id: int,
    data: schema.InvalidBidUpdateData,
    invalid_bid_interface=fastapi.Depends(db.get_invalid_bid_interface),
) -> schema.InvalidBid:

    return operations.invalid_bids.update_invalid_bid(
        invalid_bid_id, data, invalid_bid_interface
    )


@router.delete(
    "/{invalid_bid_id}",
    status_code=fastapi.status.HTTP_204_NO_CONTENT,
)
def api_delete_invalid_bid(
    invalid_bid_id: int,
    invalid_bid_interface=fastapi.Depends(db.get_invalid_bid_interface),
) -> None:

    return operations.invalid_bids.delete_invalid_bid(
        invalid_bid_id, invalid_bid_interface
    )
