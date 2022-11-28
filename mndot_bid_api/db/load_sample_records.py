from mndot_bid_api.db.database import DBSession
from tests.data.sample_db_records import bidders, bids, contracts, invalid_bids, items


def load_sample_records() -> None:
    with DBSession() as db:
        db.add_all(bidders)
        db.add_all(contracts)
        db.add_all(items)
        db.add_all(bids)
        db.add_all(invalid_bids)
        db.commit()
