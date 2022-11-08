from typing import Any

from mndot_bid_api.db import database, models
from mndot_bid_api.exceptions import (
    RecordAlreadyExistsException,
    RecordNotFoundException,
)
from sqlalchemy.orm import sessionmaker

RecordDict = dict[str, Any]


class DBModelInterface:
    def __init__(
        self, model: models.Base, configured_session_maker: sessionmaker
    ) -> None:
        self.model = model
        self.configured_session_maker = configured_session_maker

    def read_all(self) -> list[RecordDict]:
        """Returns all existing database records from the associated table."""
        with self.configured_session_maker() as db:
            records = db.query(self.model).all()
            if not records:
                return []

            return [models.to_dict(record) for record in records]

    def read_by_id(self, id: int) -> RecordDict:
        """Returns an existing database record matching the given id."""
        with self.configured_session_maker() as db:
            record = db.query(self.model).filter(self.model.id == id).first()
            if not record:
                raise RecordNotFoundException()

            return models.to_dict(record)

    def read_one_by_kwargs(self, **kwargs) -> RecordDict:
        """Returns the first existing database record that matches the given keyward arguments."""
        with self.configured_session_maker() as db:
            record = db.query(self.model).filter_by(**kwargs).first()
            if not record:
                raise RecordNotFoundException()

            return models.to_dict(record)

    def read_all_by_kwargs(self, **kwargs) -> list[RecordDict]:
        """Returns the all existing database records that match the given keyward arguments."""
        with self.configured_session_maker() as db:
            records = db.query(self.model).filter_by(**kwargs).all()
            if not records:
                raise RecordNotFoundException()

            return [models.to_dict(record) for record in records]

    def create(self, data: RecordDict) -> RecordDict:
        """Creates a new record in the database."""
        with self.configured_session_maker() as db:
            if isinstance(self.model, type(models.Item)):
                self._raise_if_item_record_exists(**data)
            else:
                record = db.query(self.model).filter_by(**data).first()
                if record:
                    raise RecordAlreadyExistsException({"id": record.id})

            new_record = self.model(**data)
            db.add(new_record)
            db.commit()

            return models.to_dict(new_record)

    def update(self, id: int, data: RecordDict) -> RecordDict:
        """Updates an existing record from the database."""
        with self.configured_session_maker() as db:
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
        with self.configured_session_maker() as db:
            record = db.query(self.model).filter(self.model.id == id).first()
            if not record:
                raise RecordNotFoundException()

            db.delete(record)
            db.commit()

    def _raise_if_item_record_exists(self, **kwargs) -> None:
        """Queries the item table for an existing record using a subset of the provided kwargs
        and raises a RecordAlreadyExistsException if one is found.

        For verifying no matching item record exists before preforming a create operation.

        Excludes the following kwargs from the query:
            - in_spec_2016
            - in_spec_2018
            - in_spec_2020
            - in_spec_2022
        """
        exclude_kwargs = [
            "in_spec_2016",
            "in_spec_2018",
            "in_spec_2020",
            "in_spec_2022",
        ]
        filtered_kwargs = {
            key: value for key, value in kwargs.items() if key not in exclude_kwargs
        }
        with self.configured_session_maker() as db:
            record = db.query(self.model).filter_by(**filtered_kwargs).first()
            if record:
                raise RecordAlreadyExistsException({"id": record.id})


def get_bidder_interface() -> DBModelInterface:
    return DBModelInterface(models.Bidder, database.DBSession)


def get_contract_interface() -> DBModelInterface:
    return DBModelInterface(models.Contract, database.DBSession)


def get_bid_interface() -> DBModelInterface:
    return DBModelInterface(models.Bid, database.DBSession)


def get_invalid_bid_interface() -> DBModelInterface:
    return DBModelInterface(models.InvalidBid, database.DBSession)


def get_item_interface() -> DBModelInterface:
    return DBModelInterface(models.Item, database.DBSession)
