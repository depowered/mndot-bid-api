import fastapi

from mndot_bid_api import db, enums, exceptions, operations, schema

router = fastapi.APIRouter(prefix="/bid", tags=["bid"])


@router.get(
    "/all",
    response_model=schema.BidCollection,
    status_code=fastapi.status.HTTP_200_OK,
)
def api_read_all_bids(
    bid_interface=fastapi.Depends(db.get_bid_interface),
) -> schema.BidCollection:

    return operations.bids.read_all_bids(bid_interface)


@router.get(
    "/{bid_id}",
    response_model=schema.Bid,
    status_code=fastapi.status.HTTP_200_OK,
)
def api_read_bid(
    bid_id: int,
    bid_interface=fastapi.Depends(db.get_bid_interface),
) -> schema.Bid:

    return operations.bids.read_bid(bid_id, bid_interface)


@router.post(
    "/",
    response_model=schema.Bid,
    status_code=fastapi.status.HTTP_201_CREATED,
)
def api_create_bid(
    data: schema.BidCreateData,
    bid_interface=fastapi.Depends(db.get_bid_interface),
    item_interface=fastapi.Depends(db.get_item_interface),
) -> schema.Bid | fastapi.responses.RedirectResponse:

    try:
        bid_result = operations.bids.create_bid(data, bid_interface, item_interface)
        return bid_result

    except exceptions.InvalidBidError:
        return fastapi.responses.RedirectResponse(
            "/invalid_bid/",
            status_code=fastapi.status.HTTP_307_TEMPORARY_REDIRECT,
        )


@router.patch(
    "/{bid_id}",
    response_model=schema.Bid,
    status_code=fastapi.status.HTTP_200_OK,
)
def api_update_bid(
    bid_id: int,
    data: schema.BidUpdateData,
    bid_interface=fastapi.Depends(db.get_bid_interface),
) -> schema.Bid:

    return operations.bids.update_bid(bid_id, data, bid_interface)


@router.delete(
    "/{bid_id}",
    status_code=fastapi.status.HTTP_204_NO_CONTENT,
)
def api_delete_bid(
    bid_id: int,
    bid_interface=fastapi.Depends(db.get_bid_interface),
):

    return operations.bids.delete_bid(bid_id, bid_interface)


@router.get(
    "/query/",
    response_model=schema.BidCollection,
    status_code=fastapi.status.HTTP_200_OK,
)
def api_query_bid(
    contract_id: int | None = None,
    item_id: int | None = None,
    bidder_id: int | None = None,
    bid_type: enums.BidType | None = None,
    bid_interface=fastapi.Depends(db.get_bid_interface),
) -> schema.BidCollection:
    kwargs = locals()

    # Filter for non-None keyword arguments to pass to the query function
    filtered_kwargs = {
        key: value for key, value in kwargs.items() if value and key != "bid_interface"
    }

    return operations.bids.query_bid(bid_interface, **filtered_kwargs)
