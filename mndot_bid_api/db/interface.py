from typing import Any

from mndot_bid_api.db import database, models
from mndot_bid_api.exceptions import (
    RecordAlreadyExistsException,
    RecordNotFoundException,
)
from overrides import override
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


class ItemInterface(DBModelInterface):
    @override
    def __init__(self, configured_session_maker: sessionmaker) -> None:
        super().__init__(models.Item, configured_session_maker)

    @override
    def create(self, data: RecordDict) -> RecordDict:
        """Creates a new record in the database."""
        with self.configured_session_maker() as db:
            # Use the non-optional ItemCreateData parameters to search for an existing record
            search_parameters = [
                "spec_code",
                "unit_code",
                "item_code",
                "short_description",
                "long_description",
                "unit",
                "unit_abbreviation",
            ]
            kwargs = {
                key: value for key, value in data.items() if key in search_parameters
            }
            record = db.query(self.model).filter_by(**kwargs).first()

            if record:
                raise RecordAlreadyExistsException({"id": record.id})

            new_record = self.model(**data)
            db.add(new_record)
            db.commit()

            return models.to_dict(new_record)


def get_bidder_interface() -> DBModelInterface:
    return DBModelInterface(models.Bidder, database.DBSession)


def get_contract_interface() -> DBModelInterface:
    return DBModelInterface(models.Contract, database.DBSession)


def get_bid_interface() -> DBModelInterface:
    return DBModelInterface(models.Bid, database.DBSession)


def get_invalid_bid_interface() -> DBModelInterface:
    return DBModelInterface(models.InvalidBid, database.DBSession)


def get_item_interface() -> DBModelInterface:
    return ItemInterface(database.DBSession)
