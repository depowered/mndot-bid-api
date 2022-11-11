from sqlalchemy.orm import sessionmaker

from mndot_bid_api.db import models


def test_add_bidder_record_rollback(configured_sessionmaker: sessionmaker):
    with configured_sessionmaker() as dbsession:
        starting_record_count = len(dbsession.query(models.Bidder).all())
        assert starting_record_count == 6

        record = models.Bidder(id=-100, name="Record to rollback")
        dbsession.add(record)

        ending_record_count = len(dbsession.query(models.Bidder).all())
        assert ending_record_count == 7


def test_bidder_record_count_after_rollback(configured_sessionmaker: sessionmaker):
    with configured_sessionmaker() as dbsession:
        starting_record_count = len(dbsession.query(models.Bidder).all())
        assert starting_record_count == 6
