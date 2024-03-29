from typing import Any

from sqlalchemy.orm import sessionmaker

from mndot_bid_api.db import database, models
from mndot_bid_api.exceptions import RecordAlreadyExistsError, RecordNotFoundError

RecordDict = dict[str, Any]


class DBModelInterface:
    """Interface that abstracts database calls for Create, Read, Update, and Delete operations."""

    def __init__(
        self, model: models.Base, configured_sessionmaker: sessionmaker
    ) -> None:
        self.model = model
        self.configured_sessionmaker = configured_sessionmaker

    def read_all(self, limit: int = 0) -> list[RecordDict]:
        """Returns all existing database records from the associated table.

        Limit values:
         - Negative: Returns no records
         - Zero: Returns all records (default)
         - Positive: Returns a number of records equal to the limit
        """
        if limit < 0:
            return []

        with self.configured_sessionmaker() as db:
            records = None
            if limit > 0:
                records = db.query(self.model).limit(limit).all()
            else:
                records = db.query(self.model).all()

            if not records:
                return []

            return [models.to_dict(record) for record in records]

    def read_by_id(self, id: int) -> RecordDict:
        """Returns an existing database record matching the given id."""
        with self.configured_sessionmaker() as db:
            record = db.query(self.model).filter(self.model.id == id).first()
            if not record:
                raise RecordNotFoundError()

            return models.to_dict(record)

    def read_one_by_kwargs(self, **kwargs) -> RecordDict:
        """Returns the first existing database record that matches the given keyward arguments."""
        with self.configured_sessionmaker() as db:
            record = db.query(self.model).filter_by(**kwargs).first()
            if not record:
                raise RecordNotFoundError()

            return models.to_dict(record)

    def read_all_by_kwargs(self, limit: int = 0, **kwargs) -> list[RecordDict]:
        """Returns the all existing database records that match the given keyward arguments.

        Limit values:
         - Negative: Returns no records
         - Zero: Returns all records (default)
         - Positive: Returns a number of records equal to the limit
        """
        if limit < 0:
            return []

        with self.configured_sessionmaker() as db:
            records = None
            if limit > 0:
                records = db.query(self.model).filter_by(**kwargs).limit(limit).all()
            else:
                records = db.query(self.model).filter_by(**kwargs).all()
            if not records:
                raise RecordNotFoundError()

            return [models.to_dict(record) for record in records]

    def create(self, data: RecordDict) -> RecordDict:
        """Creates a new record in the database."""
        with self.configured_sessionmaker() as db:
            record = None

            if isinstance(self.model(), models.Item):
                # Query with a subset of fields in data
                self._raise_if_item_record_exists(**data)
            elif isinstance(self.model(), models.Bid) or isinstance(
                self.model(), models.InvalidBid
            ):
                # Query with all fields of data
                record = db.query(self.model).filter_by(**data).first()
            else:
                # Query by id
                record = db.query(self.model).filter_by(id=data.get("id")).first()

            if record:
                raise RecordAlreadyExistsError({"id": record.id})

            new_record = self.model(**data)
            db.add(new_record)
            db.commit()

            return models.to_dict(new_record)

    def update(self, id: int, data: RecordDict) -> RecordDict:
        """Updates an existing record from the database."""
        with self.configured_sessionmaker() as db:
            record = db.query(self.model).filter(self.model.id == id).first()
            if not record:
                raise RecordNotFoundError()

            for key, value in data.items():
                setattr(record, key, value)

            db.add(record)
            db.commit()

            return models.to_dict(record)

    def delete(self, id: int) -> None:
        """Deletes an existing record from the database."""
        with self.configured_sessionmaker() as db:
            record = db.query(self.model).filter(self.model.id == id).first()
            if not record:
                raise RecordNotFoundError()

            db.delete(record)
            db.commit()

    def _raise_if_item_record_exists(self, **kwargs) -> None:
        """Queries the item table for an existing record using a subset of the provided kwargs
        and raises a RecordAlreadyExistsError if one is found.

        For verifying no matching item record exists before preforming a create operation.

        Includes the following kwargs from the query:
            - spec_code
            - unit_code
            - item_code
            - short_description
            - long_description
            - unit
            - unit_abbreviation
        """
        include_kwargs = [
            "spec_code",
            "unit_code",
            "item_code",
            "short_description",
            "long_description",
            "unit",
            "unit_abbreviation",
        ]
        filtered_kwargs = {
            key: value for key, value in kwargs.items() if key in include_kwargs
        }
        with self.configured_sessionmaker() as db:
            record = db.query(self.model).filter_by(**filtered_kwargs).first()
            if record:
                raise RecordAlreadyExistsError({"id": record.id})


def get_bidder_interface() -> DBModelInterface:
    """Return a DBModelInterface configured for Bidder model operations."""
    return DBModelInterface(models.Bidder, database.DBSession)


def get_contract_interface() -> DBModelInterface:
    """Return a DBModelInterface configured for Contract model operations."""
    return DBModelInterface(models.Contract, database.DBSession)


def get_bid_interface() -> DBModelInterface:
    """Return a DBModelInterface configured for Bid model operations."""
    return DBModelInterface(models.Bid, database.DBSession)


def get_invalid_bid_interface() -> DBModelInterface:
    """Return a DBModelInterface configured for Invalid Bid model operations."""
    return DBModelInterface(models.InvalidBid, database.DBSession)


def get_item_interface() -> DBModelInterface:
    """Return a DBModelInterface configured for Item model operations."""
    return DBModelInterface(models.Item, database.DBSession)
