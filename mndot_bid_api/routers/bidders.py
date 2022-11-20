import fastapi

from mndot_bid_api import db, operations, schema

router = fastapi.APIRouter(prefix="/bidder", tags=["bidder"])


@router.get(
    "/all",
    response_model=schema.BidderCollection,
    status_code=fastapi.status.HTTP_200_OK,
)
def api_read_all_bidders(
    bidder_interface=fastapi.Depends(db.get_bidder_interface),
) -> schema.BidderCollection:

    return operations.bidders.read_all_bidders(bidder_interface)


@router.get(
    "/{bidder_id}",
    response_model=schema.Bidder,
    status_code=fastapi.status.HTTP_200_OK,
)
def api_read_bidder(
    bidder_id: int,
    bidder_interface=fastapi.Depends(db.get_bidder_interface),
) -> schema.Bidder:

    return operations.bidders.read_bidder(bidder_id, bidder_interface)


@router.post(
    "/",
    response_model=schema.Bidder,
    status_code=fastapi.status.HTTP_200_OK,
)
def api_create_bidder(
    data: schema.BidderCreateData,
    bidder_interface=fastapi.Depends(db.get_bidder_interface),
) -> schema.Bidder:

    return operations.bidders.create_bidder(data, bidder_interface)


@router.patch(
    "/{bidder_id}",
    response_model=schema.Bidder,
    status_code=fastapi.status.HTTP_200_OK,
)
def api_update_bidder(
    bidder_id: int,
    data: schema.BidderUpdateData,
    bidder_interface=fastapi.Depends(db.get_bidder_interface),
) -> schema.Bidder:

    return operations.bidders.update_bidder(bidder_id, data, bidder_interface)


@router.delete(
    "/{bidder_id}",
    status_code=fastapi.status.HTTP_204_NO_CONTENT,
)
def api_delete_bidder(
    bidder_id: int,
    bidder_interface=fastapi.Depends(db.get_bidder_interface),
):

    return operations.bidders.delete_bidder(bidder_id, bidder_interface)


@router.get(
    "/query/",
    response_model=schema.BidderCollection,
    status_code=fastapi.status.HTTP_200_OK,
)
def api_query_bidder(
    name: str | None = None, bidder_interface=fastapi.Depends(db.get_bidder_interface)
) -> schema.BidderCollection:
    kwargs = locals()

    # Filter for non-None keyword arguments to pass to the query function
    filtered_kwargs = {
        key: value
        for key, value in kwargs.items()
        if value and key != "bidder_interface"
    }

    return operations.bidders.query_bidder(bidder_interface, **filtered_kwargs)
