from datetime import datetime

from mndot_bid_api.db import database
from mndot_bid_api.db.models import Bid, Bidder, Contract

bidders = [
    Bidder(id=1, name="Veit"),
    Bidder(id=2, name="S.M. Hentges and Sons"),
    Bidder(id=3, name="Ames"),
]

# contracts = [
#     Contract(
#         id=1,
#         is_processed=True,
#         let_date=datetime.today(),
#         let_year=2022,
#         spec_year=2020,
#         sp_number="4911-15",
#         district="Baxter",
#         county="Benton",
#         engineers_total=2_000_000_00,
#         lowest_bidder_id=3,
#         lowest_bidder_total=2_500_000_00,
#     ),
#     Contract(id=2, is_processed=False),
#     Contract(id=3, is_processed=False),
# ]

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
        db.commit()
