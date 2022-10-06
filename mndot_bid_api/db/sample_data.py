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

# bids = [
#     Bid(
#         id=1,
#         item_number="2501.503/02931",
#         spec_year=2020,
#         quantity=300.0,
#         unit_price=6_00,
#         total_price=int(300.0 * 6_00),
#         contract_id=1,
#         bidder_id=3,
#         bidder_rank=1,
#     ),
#     Bid(
#         id=2,
#         item_number="2575.503/12345",
#         spec_year=2020,
#         quantity=10_000.0,
#         unit_price=1_25,
#         total_price=int(10_000.0 * 1_25),
#         contract_id=1,
#         bidder_id=3,
#         bidder_rank=1,
#     ),
#     Bid(
#         id=3,
#         item_number="2575.501/00010",
#         spec_year=2020,
#         quantity=1.0,
#         unit_price=30_000_00,
#         total_price=int(1.0 * 30_000_00),
#         contract_id=1,
#         bidder_id=3,
#         bidder_rank=1,
#     ),
# ]


def load_sample_data() -> None:
    with database.DBSession() as db:
        db.add_all(bidders)
        db.add_all(contracts)
        db.commit()
