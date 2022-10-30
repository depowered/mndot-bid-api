from typing import Any

from mndot_bid_api.db import database, models
from mndot_bid_api.exceptions import (
    RecordAlreadyExistsException,
    RecordNotFoundException,
)

RecordDict = dict[str, Any]


class DBModelInterface:
    def __init__(self, model: models.Base) -> None:
        self.model = model

    def read_all(self) -> list[RecordDict]:
        """Returns all existing database records from the associated table."""
        with database.SessionContextManager() as db:
            records = db.query(self.model).all()
            if not records:
                return []

            return [models.to_dict(record) for record in records]

    def read_by_id(self, id: int) -> RecordDict:
        """Returns an existing database record matching the given id."""
        with database.SessionContextManager() as db:
            record = db.query(self.model).filter(self.model.id == id).first()
            if not record:
                raise RecordNotFoundException()

            return models.to_dict(record)

    def create(self, data: RecordDict) -> RecordDict:
        """Creates a new record in the database."""
        with database.SessionContextManager() as db:
            # Statement valid only if data parameter includes an id key
            record = db.query(self.model).filter(self.model.id == data["id"]).first()
            if record:
                raise RecordAlreadyExistsException()

            new_record = self.model(**data)
            db.add(new_record)
            db.commit()

            return models.to_dict(new_record)

    def update(self, id: int, data: RecordDict) -> RecordDict:
        """Updates an existing record from the database."""
        with database.SessionContextManager() as db:
            record = db.query(self.model).filter(self.model.id == id).first()
            if not record:
                raise RecordNotFoundException()

            for key, value in data.items():
                setattr(record, key, value)

            db.add(record)
            db.commit()

            return models.to_dict(record)

    def delete(self, id: int) -> None:
        """Deletes an existing record from the database."""
        with database.SessionContextManager() as db:
            record = db.query(self.model).filter(self.model.id == id).first()
            if not record:
                raise RecordNotFoundException()

            db.delete(record)
            db.commit()


def get_bidder_interface() -> DBModelInterface:
    return DBModelInterface(models.Bidder)
