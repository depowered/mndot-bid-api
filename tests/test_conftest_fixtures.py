from mndot_bid_api.db import models
from sqlalchemy.orm import Session


def test_add_bidder_record_rollback(dbsession: Session):
    starting_record_count = len(dbsession.query(models.Bidder).all())
    assert starting_record_count == 6

    record = models.Bidder(id=-100, name="Record to rollback")
    dbsession.add(record)

    ending_record_count = len(dbsession.query(models.Bidder).all())
    assert ending_record_count == 7


def test_bidder_record_count_after_rollback(dbsession: Session):
    starting_record_count = len(dbsession.query(models.Bidder).all())
    assert starting_record_count == 6
