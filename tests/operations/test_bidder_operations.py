import fastapi
import pytest

from mndot_bid_api import operations
from mndot_bid_api.exceptions import (
    RecordAlreadyExistsException,
    RecordNotFoundException,
)
from mndot_bid_api.operations import schema
from mndot_bid_api.operations.crud_interface import RecordDict

sample_bidders = [
    {"id": 0, "name": "engineer"},
    {"id": 207897, "name": "Central Specialties, Inc."},
    {"id": 192907, "name": "NorthStar Materials, Inc. DBA Knife River Materials"},
    {"id": 857140, "name": "Anderson Brothers Construction Company of Brainerd, LLC"},
    {"id": 215861, "name": None},
    {"id": 197466, "name": None},
]

VALID_BIDDER_ID = 207897
INVALID_BIDDER_ID = -7


class BidderCRUDInterfaceStub:
    def read_all(self) -> list[RecordDict]:
        return sample_bidders

    def read_by_id(self, id: int) -> RecordDict:
        if id == VALID_BIDDER_ID:
            return sample_bidders[1]
        else:
            raise RecordNotFoundException()

    def read_one_by_kwargs(self, **kwargs) -> RecordDict:
        raise NotImplementedError()

    def read_all_by_kwargs(self, **kwargs) -> list[RecordDict]:
        if kwargs.get("name") == sample_bidders[1]["name"]:
            return [sample_bidders[1]]
        else:
            raise RecordNotFoundException()

    def create(self, data: RecordDict) -> RecordDict:
        if data in sample_bidders:
            raise RecordAlreadyExistsException()
        return data

    def update(self, id: int, data: RecordDict) -> RecordDict:
        if id == VALID_BIDDER_ID:
            record = sample_bidders[1].copy()
            record.update(**data)
            return record
        else:
            raise RecordNotFoundException()

    def delete(self, id: int) -> None:
        if id == VALID_BIDDER_ID:
            return None
        else:
            raise RecordNotFoundException()


bidder_interface_stub = BidderCRUDInterfaceStub()


def test_read_all_bidders():
    result = operations.bidders.read_all_bidders(bidder_interface_stub)
    assert result.type == "BidderCollection"
    assert len(result.data) == 6


def test_read_bidder_by_id():
    result = operations.bidders.read_bidder(VALID_BIDDER_ID, bidder_interface_stub)
    assert result.type == "Bidder"
    assert result.data.id == VALID_BIDDER_ID
    assert result.data.name is "Central Specialties, Inc."

    with pytest.raises(fastapi.HTTPException) as exc:
        operations.bidders.read_bidder(INVALID_BIDDER_ID, bidder_interface_stub)
    assert exc.value.status_code == 404


def test_create_bidder():
    new_record_data = schema.BidderCreateData(id=100, name="Test Name")
    result = operations.bidders.create_bidder(new_record_data, bidder_interface_stub)

    assert result.type == "Bidder"
    assert result.data.id == new_record_data.id
    assert result.data.name == new_record_data.name

    record_already_exists_data = schema.BidderCreateData(**sample_bidders[0])
    with pytest.raises(fastapi.HTTPException) as exc:
        operations.bidders.create_bidder(
            record_already_exists_data, bidder_interface_stub
        )
    assert exc.value.status_code == 303


def test_update_bidder():
    bidder_update_data = schema.BidderUpdateData(name="Parking Lot Pavers, Inc.")
    result = operations.bidders.update_bidder(
        VALID_BIDDER_ID, bidder_update_data, bidder_interface_stub
    )

    assert result.type == "Bidder"
    assert result.data.id == VALID_BIDDER_ID
    assert result.data.name == bidder_update_data.name

    with pytest.raises(fastapi.HTTPException) as exc:
        operations.bidders.update_bidder(
            INVALID_BIDDER_ID, bidder_update_data, bidder_interface_stub
        )
    assert exc.value.status_code == 404


def test_delete_bidder():
    try:
        operations.bidders.delete_bidder(VALID_BIDDER_ID, bidder_interface_stub)
    except Exception as exc:
        assert (
            False
        ), f"delete_bidder raised an unexpected execption: {type(exc).__name__}"

    with pytest.raises(fastapi.HTTPException) as exc:
        operations.bidders.delete_bidder(INVALID_BIDDER_ID, bidder_interface_stub)
    assert exc.value.status_code == 404


def test_query_bidder():
    bidder_name = sample_bidders[1]["name"]
    result = operations.bidders.query_bidder(bidder_interface_stub, name=bidder_name)

    assert result.type == "BidderCollection"
    assert len(result.data) == 1
    assert result.data[0].id == VALID_BIDDER_ID
    assert result.data[0].name == bidder_name

    with pytest.raises(fastapi.HTTPException) as exc:
        operations.bidders.query_bidder(bidder_interface_stub)
    assert exc.value.status_code == 400

    with pytest.raises(fastapi.HTTPException) as exc:
        operations.bidders.query_bidder(
            bidder_interface_stub, name="Not an existing name"
        )
    assert exc.value.status_code == 404
