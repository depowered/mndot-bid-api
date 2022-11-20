import fastapi

from mndot_bid_api import db, enums, operations, schema

invalid_bid_router = fastapi.APIRouter(prefix="/invalid_bid", tags=["invalid_bid"])


@invalid_bid_router.get(
    "/all",
    response_model=schema.InvalidBidCollection,
    status_code=fastapi.status.HTTP_200_OK,
)
def api_read_all_invalid_bids(
    invalid_bid_interface=fastapi.Depends(db.get_invalid_bid_interface),
) -> schema.InvalidBidCollection:

    return operations.invalid_bids.read_all_invalid_bids(invalid_bid_interface)


@invalid_bid_router.get(
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


@invalid_bid_router.post(
    "/",
    response_model=schema.InvalidBid,
    status_code=fastapi.status.HTTP_201_CREATED,
)
def api_create_invalid_bid(
    data: schema.BidCreateData,
    invalid_bid_interface=fastapi.Depends(db.get_invalid_bid_interface),
) -> schema.InvalidBid:

    return operations.invalid_bids.create_invalid_bid(data, invalid_bid_interface)


@invalid_bid_router.patch(
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


@invalid_bid_router.delete(
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


@invalid_bid_router.get(
    "/query/",
    response_model=schema.InvalidBidCollection,
    status_code=fastapi.status.HTTP_200_OK,
)
def api_query_invalid_bid(
    invalid_bid_interface=fastapi.Depends(db.get_invalid_bid_interface),
    contract_id: int | None = None,
    bidder_id: int | None = None,
    item_spec_code: str | None = None,
    item_unit_code: str | None = None,
    item_item_code: str | None = None,
    item_long_description: str | None = None,
    item_unit_abbreviation: str | None = None,
    quantity: float | None = None,
    unit_price: int | None = None,
    bid_type: enums.BidType | None = None,
) -> schema.InvalidBidCollection:
    kwargs = locals()

    # Filter for non-None keyword arguments to pass to the query function
    filtered_kwargs = {
        key: value
        for key, value in kwargs.items()
        if value and key != "invalid_bid_interface"
    }

    return operations.invalid_bids.query_invalid_bid(
        invalid_bid_interface, **filtered_kwargs
    )
