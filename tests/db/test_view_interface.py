from sqlalchemy.orm import sessionmaker

from mndot_bid_api.db.views import ViewInterface
from mndot_bid_api.schema import WeightedAvgUnitPrice


def test_weighted_avg_bid_prices_by_year(configured_sessionmaker):
    expected = [
        WeightedAvgUnitPrice(
            item_id=2,
            year=2022,
            bid_type="engineer",
            weighted_avg_unit_price=(15_42 / 100),
            occurances=1,
        ),
        WeightedAvgUnitPrice(
            item_id=2,
            year=2022,
            bid_type="winning",
            weighted_avg_unit_price=(8_00 / 100),
            occurances=1,
        ),
        WeightedAvgUnitPrice(
            item_id=2,
            year=2022,
            bid_type="losing",
            weighted_avg_unit_price=(27_13 / 4 / 100),
            occurances=1,
        ),
    ]

    interface = ViewInterface(configured_sessionmaker)
    results = interface.weighted_avg_bid_prices_by_year(item_id=2)

    assert isinstance(results, list)
    assert len(results) == len(expected)

    # results won't necessarily match the order of expected so we preform some iterative matching here
    for item in results:
        if item.bid_type == "engineer":
            assert item.weighted_avg_unit_price == expected[0].weighted_avg_unit_price
        if item.bid_type == "winning":
            assert item.weighted_avg_unit_price == expected[1].weighted_avg_unit_price
        if item.bid_type == "losing":
            assert item.weighted_avg_unit_price == expected[2].weighted_avg_unit_price


def test_all_contract_ids(configured_sessionmaker: sessionmaker):
    interface = ViewInterface(configured_sessionmaker)
    contact_ids = interface.all_contract_ids()

    assert isinstance(contact_ids, list)
    assert len(contact_ids) == 1
