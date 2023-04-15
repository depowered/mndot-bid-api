from sqlalchemy.orm import sessionmaker

from mndot_bid_api.db.views import ViewInterface


def test_all_contract_ids(configured_sessionmaker: sessionmaker):
    interface = ViewInterface(configured_sessionmaker)
    contact_ids = interface.all_contract_ids()

    assert isinstance(contact_ids, list)
    assert len(contact_ids) == 1
