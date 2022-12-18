import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker

from mndot_bid_api.schema import AverageBidPrice
from mndot_bid_api.db import database, models


class ViewInterface:
    def __init__(self, configured_sessionmaker: sessionmaker) -> None:
        self.configured_sessionmaker = configured_sessionmaker

    def avg_bid_prices(self, item_id) -> list[AverageBidPrice]:
        view = (
            sa.select(
                models.Bid.item_id.label("item_id"),
                sa.extract("year", models.Contract.letting_date).label("year"),
                models.Bid.bid_type.label("bid_type"),
                (
                    sa.func.sum(models.Bid.quantity * models.Bid.unit_price)
                    / sa.func.sum(models.Bid.quantity)
                    / 100
                ).label("avg_unit_price"),
                sa.func.count(models.Bid.contract_id).label("occurances"),
            )
            .join(models.Contract, models.Bid.contract_id == models.Contract.id)
            .group_by("item_id", "year", "bid_type")
        )

        with self.configured_sessionmaker() as session:
            results = session.execute(view.where(models.Bid.item_id == item_id))
            return [AverageBidPrice(**row) for row in results.all()]


def get_view_interface() -> ViewInterface:
    return ViewInterface(database.DBSession)
