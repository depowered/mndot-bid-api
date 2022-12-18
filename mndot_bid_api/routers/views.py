import fastapi

from mndot_bid_api import db, operations, schema

view_router = fastapi.APIRouter(prefix="/view", tags=["view"])


@view_router.get(
    "/avg_bid_prices/{item_id}",
    response_model=list[schema.WeightedAvgUnitPrice],
    status_code=fastapi.status.HTTP_200_OK,
)
def api_weighted_avg_bid_prices_by_year(
    item_id: int,
    view_interface=fastapi.Depends(db.get_view_interface),
) -> list[schema.WeightedAvgUnitPrice]:

    return operations.views.weighted_avg_bid_prices_by_year(item_id, view_interface)
