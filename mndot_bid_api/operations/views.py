from mndot_bid_api import schema
from mndot_bid_api.operations.view_interface import ViewInterface


def weighted_avg_bid_prices_by_year(
    item_id: int, view_interface: ViewInterface
) -> list[schema.WeightedAvgUnitPrice]:

    return view_interface.weighted_avg_bid_prices_by_year(item_id)
