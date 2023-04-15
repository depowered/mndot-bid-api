import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker

from mndot_bid_api.db import database, models
from mndot_bid_api.schema import WeightedAvgUnitPrice


class ViewInterface:
    def __init__(self, configured_sessionmaker: sessionmaker) -> None:
        self.configured_sessionmaker = configured_sessionmaker

    def weighted_avg_bid_prices_by_year(self, item_id) -> list[WeightedAvgUnitPrice]:
        view = (
            sa.select(
                models.Bid.item_id.label("item_id"),
                sa.extract("year", models.Contract.letting_date).label("year"),
                models.Bid.bid_type.label("bid_type"),
                (
                    sa.func.sum(models.Bid.quantity * models.Bid.unit_price)
                    / sa.func.sum(models.Bid.quantity)
                    / 100
                ).label("weighted_avg_unit_price"),
                sa.func.count(models.Bid.contract_id).label("occurances"),
            )
            .join(models.Contract, models.Bid.contract_id == models.Contract.id)
            .group_by("item_id", "year", "bid_type")
        )

        with self.configured_sessionmaker() as session:
            results = session.execute(view.where(models.Bid.item_id == item_id))
            return [WeightedAvgUnitPrice(**row) for row in results.all()]

    def all_contract_ids(self) -> list[int]:
        query = sa.select(models.Contract.id.label("contract_id"))
        with self.configured_sessionmaker() as session:
            results = session.execute(query)
            return [row.contract_id for row in results.all()]


def get_view_interface() -> ViewInterface:
    return ViewInterface(database.DBSession)
