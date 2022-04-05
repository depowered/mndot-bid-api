from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from mndot_bid_api.db.models import Base
from mndot_bid_api.db.sample_data import bidders, contracts, bids


def create_db(file: str):
    engine = create_engine(file)
    Base.metadata.create_all(engine)

    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    session.add_all(bidders)
    session.add_all(contracts)
    session.add_all(bids)

    session.commit()
