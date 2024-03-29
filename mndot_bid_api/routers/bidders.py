import fastapi

from mndot_bid_api import auth, db, operations, schema

bidder_router = fastapi.APIRouter(prefix="/bidder", tags=["bidder"])


@bidder_router.get(
    "/all",
    response_model=schema.BidderCollection,
    status_code=fastapi.status.HTTP_200_OK,
)
def api_read_all_bidders(
    limit: int = 100,
    bidder_interface=fastapi.Depends(db.get_bidder_interface),
) -> schema.BidderCollection:

    return operations.bidders.read_all_bidders(limit, bidder_interface)


@bidder_router.get(
    "/{bidder_id}",
    response_model=schema.Bidder,
    status_code=fastapi.status.HTTP_200_OK,
)
def api_read_bidder(
    bidder_id: int,
    bidder_interface=fastapi.Depends(db.get_bidder_interface),
) -> schema.Bidder:

    return operations.bidders.read_bidder(bidder_id, bidder_interface)


@bidder_router.post(
    "/",
    response_model=schema.Bidder,
    status_code=fastapi.status.HTTP_200_OK,
)
def api_create_bidder(
    data: schema.BidderCreateData,
    bidder_interface=fastapi.Depends(db.get_bidder_interface),
    api_key: auth.APIKeyHeader = fastapi.Depends(auth.authorize_api_key),
) -> schema.Bidder:

    return operations.bidders.create_bidder(data, bidder_interface)


@bidder_router.patch(
    "/{bidder_id}",
    response_model=schema.Bidder,
    status_code=fastapi.status.HTTP_200_OK,
)
def api_update_bidder(
    bidder_id: int,
    data: schema.BidderUpdateData,
    bidder_interface=fastapi.Depends(db.get_bidder_interface),
    api_key: auth.APIKeyHeader = fastapi.Depends(auth.authorize_api_key),
) -> schema.Bidder:

    return operations.bidders.update_bidder(bidder_id, data, bidder_interface)


@bidder_router.delete(
    "/{bidder_id}",
    status_code=fastapi.status.HTTP_204_NO_CONTENT,
)
def api_delete_bidder(
    bidder_id: int,
    bidder_interface=fastapi.Depends(db.get_bidder_interface),
    api_key: auth.APIKeyHeader = fastapi.Depends(auth.authorize_api_key),
):

    return operations.bidders.delete_bidder(bidder_id, bidder_interface)


@bidder_router.get(
    "/query/",
    response_model=schema.BidderCollection,
    status_code=fastapi.status.HTTP_200_OK,
)
def api_query_bidder(
    name: str | None = None,
    bidder_interface=fastapi.Depends(db.get_bidder_interface),
    limit: int = 100,
) -> schema.BidderCollection:
    kwargs = locals()

    # Filter for non-None keyword arguments to pass to the query function
    filtered_kwargs = {
        key: value
        for key, value in kwargs.items()
        if value and key not in ["bidder_interface", "limit"]
    }

    return operations.bidders.query_bidder(bidder_interface, limit, **filtered_kwargs)
