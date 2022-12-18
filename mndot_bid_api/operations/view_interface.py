from typing import Protocol

from mndot_bid_api import schema


class ViewInterface(Protocol):
    def weighted_avg_bid_prices_by_year(
        self, item_id: int
    ) -> list[schema.WeightedAvgUnitPrice]:
        ...
