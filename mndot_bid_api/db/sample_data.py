from datetime import datetime

from mndot_bid_api.db import database, models

bidders = [
    models.Bidder(id=1, name="Veit"),
    models.Bidder(id=2, name="S.M. Hentges and Sons"),
    models.Bidder(id=3, name="Ames"),
]

contracts = [
    models.Contract(
        id=1,
        letting_date=datetime.today(),
        sp_number="4911-15",
        district="Baxter",
        county="Benton",
        description="Some road is getting new pavement",
        winning_bidder_id=1,
        spec_year=2020,
    ),
    models.Contract(
        id=2,
        letting_date=datetime.today(),
        sp_number="3309-35",
        district="Metro",
        county="Hennepin",
        description="They build ponds for this one",
        winning_bidder_id=3,
        spec_year=2020,
    ),
]

bids = [
    models.Bid(
        id=1,
        contract_id=2,
        item_composite_id="2020_2501_503_02931",
        bidder_id=3,
        quantity=300.0,
        unit_price=6_00,
        bid_type="winning_bid",
    ),
    models.Bid(
        id=2,
        contract_id=2,
        item_composite_id="2020_2575_503_12345",
        bidder_id=3,
        quantity=10_000.0,
        unit_price=1_25,
        bid_type="winning_bid",
    ),
    models.Bid(
        id=3,
        contract_id=2,
        item_composite_id="2020_2575_501_00010",
        bidder_id=3,
        quantity=1.0,
        unit_price=30_000_00,
        bid_type="winning_bid",
    ),
    models.Bid(
        id=4,
        contract_id=2,
        item_composite_id="2020_2501_503_02931",
        bidder_id=0,
        quantity=300.0,
        unit_price=int(6_00 * 1.2),
        bid_type="engineers_estimate",
    ),
    models.Bid(
        id=5,
        contract_id=2,
        item_composite_id="2020_2575_503_12345",
        bidder_id=0,
        quantity=10_000.0,
        unit_price=int(1_25 * 1.2),
        bid_type="engineers_estimate",
    ),
    models.Bid(
        id=6,
        contract_id=2,
        item_composite_id="2020_2575_501_00010",
        bidder_id=0,
        quantity=1.0,
        unit_price=int(30_000_00 * 1.2),
        bid_type="engineers_estimate",
    ),
]


items = [
    models.Item(
        id=1,
        composite_id="2501_503_02931",
        spec_year="2020",
        spec_code="2501",
        unit_code="503",
        item_code="02931",
        short_description="biolog",
        long_description="sediment control log type (straw)",
        unit="LIN FT",
        unit_abbreviation="LF",
    ),
    models.Item(
        id=2,
        composite_id="2575_501_00010",
        spec_year="2020",
        spec_code="2575",
        unit_code="501",
        item_code="00010",
        short_description="silt fence",
        long_description="silt fence type HI",
        unit="LIN FT",
        unit_abbreviation="LF",
    ),
    models.Item(
        id=3,
        composite_id="2501_503_02931",
        spec_year="2018",
        spec_code="2501",
        unit_code="503",
        item_code="02931",
        short_description="biolog",
        long_description="sediment control log type (straw)",
        unit="LIN FT",
        unit_abbreviation="LF",
    ),
    models.Item(
        id=4,
        composite_id="2018_2575_501_00010",
        spec_year="2018",
        spec_code="2575",
        unit_code="501",
        item_code="00010",
        short_description="silt fence",
        long_description="silt fence type HI",
        unit="LIN FT",
        unit_abbreviation="LF",
    ),
    models.Item(
        id=5,
        composite_id="2501_503_02931",
        spec_year="2016",
        spec_code="2501",
        unit_code="503",
        item_code="02931",
        short_description="biolog",
        long_description="sediment control log type (straw)",
        unit="LIN FT",
        unit_abbreviation="LF",
    ),
    models.Item(
        id=6,
        composite_id="2575_501_00010",
        spec_year="2016",
        spec_code="2575",
        unit_code="501",
        item_code="00010",
        short_description="silt fence",
        long_description="silt fence type HI",
        unit="LIN FT",
        unit_abbreviation="LF",
    ),
]


def load_sample_data() -> None:
    with database.DBSession() as db:
        db.add_all(bidders)
        db.add_all(contracts)
        db.add_all(bids)
        db.add_all(items)
        db.commit()
