from datetime import date

import fastapi
import pytest
from mndot_bid_api import operations
from mndot_bid_api.exceptions import (
    RecordAlreadyExistsException,
    RecordNotFoundException,
)
from mndot_bid_api.operations import enums, schema
from mndot_bid_api.operations.crud_interface import RecordDict

sample_contracts = [
    {
        "id": 220005,
        "letting_date": date(year=2022, month=1, day=28),
        "sp_number": "5625-20",
        "district": "Detroit Lakes",
        "county": "Otter Tail",
        "description": "LOCATED ON T.H. 108 FROM 420' WEST OF EB T.H. 94 RAMP TO 9TH ST NW.",
        "winning_bidder_id": 207897,
    },
]

VALID_CONTRACT_ID = 220005
INVALID_CONTRACT_ID = -7


class ContractCRUDInterfaceStub:
    def read_all(self) -> list[RecordDict]:
        return sample_contracts

    def read_by_id(self, id: int) -> RecordDict:
        if id == VALID_CONTRACT_ID:
            return sample_contracts[0]
        raise RecordNotFoundException()

    def read_one_by_kwargs(self, **kwargs) -> RecordDict:
        raise NotImplementedError()

    def read_all_by_kwargs(self, **kwargs) -> list[RecordDict]:
        if kwargs.get("district"):
            return sample_contracts
        else:
            raise RecordNotFoundException()

    def create(self, data: RecordDict) -> RecordDict:
        if data in sample_contracts:
            raise RecordAlreadyExistsException()
        return data

    def update(self, id: int, data: RecordDict) -> RecordDict:
        if id == VALID_CONTRACT_ID:
            record = sample_contracts[0].copy()
            record.update(**data)
            return record
        else:
            raise RecordNotFoundException()

    def delete(self, id: int) -> None:
        if id == VALID_CONTRACT_ID:
            return None
        else:
            raise RecordNotFoundException()


contract_interface_stub = ContractCRUDInterfaceStub()


def test_read_all_contracts():
    result = operations.contracts.read_all_contracts(contract_interface_stub)
    assert result.type == "ContractCollection"
    assert len(result.data) == 1


def test_read_contract_by_id():
    result = operations.contracts.read_contract(
        VALID_CONTRACT_ID, contract_interface_stub
    )
    assert result.type == "Contract"
    assert result.data.id == VALID_CONTRACT_ID
    assert result.data.letting_date == date(year=2022, month=1, day=28)

    with pytest.raises(fastapi.HTTPException) as exc:
        operations.contracts.read_contract(-7, contract_interface_stub)
    assert exc.value.status_code == 404


def test_create_contract():
    new_record_data = schema.ContractCreateData(
        id=220002,
        letting_date=date(year=2022, month=1, day=28),
        sp_number="0803-44",
        district=enums.District.MANKATO,
        county=enums.County.BROWN,
        description="LOCATED ON T.H. 14 FROM 490' WEST OF T.H. 71 TO 0.23 MILES EAST OF CSAH 5.",
        winning_bidder_id=198793,
    )
    result = operations.contracts.create_contract(
        new_record_data, contract_interface_stub
    )

    assert result.type == "Contract"
    assert result.data.id == new_record_data.id
    assert result.data.letting_date == date(year=2022, month=1, day=28)

    record_already_exists_data = schema.ContractCreateData(**sample_contracts[0])
    with pytest.raises(fastapi.HTTPException) as exc:
        operations.contracts.create_contract(
            record_already_exists_data, contract_interface_stub
        )
    assert exc.value.status_code == 303


def test_update_contract():
    contract_id = 220005
    contract_update_data = schema.ContractUpdateData(
        letting_date=date(year=1901, month=12, day=25),
        winning_bidder_id=101,
    )
    result = operations.contracts.update_contract(
        VALID_CONTRACT_ID, contract_update_data, contract_interface_stub
    )

    assert result.type == "Contract"
    assert result.data.id == contract_id
    assert result.data.letting_date == contract_update_data.letting_date
    assert result.data.winning_bidder_id == contract_update_data.winning_bidder_id

    with pytest.raises(fastapi.HTTPException) as exc:
        operations.contracts.update_contract(
            INVALID_CONTRACT_ID, contract_update_data, contract_interface_stub
        )
    assert exc.value.status_code == 404


def test_delete_contract():
    try:
        operations.contracts.delete_contract(VALID_CONTRACT_ID, contract_interface_stub)
    except Exception as exc:
        assert (
            False
        ), f"delete_contract raised an unexcpected exception: {type(exc).__name__}"

    with pytest.raises(fastapi.HTTPException) as exc:
        operations.contracts.delete_contract(
            INVALID_CONTRACT_ID, contract_interface_stub
        )
    assert exc.value.status_code == 404


def test_query_contract():
    district = "Detroit Lakes"
    result = operations.contracts.query_contract(
        contract_interface_stub, district=district
    )

    assert result.type == "ContractCollection"
    assert len(result.data) == 1
    assert result.data[0].id == VALID_CONTRACT_ID
    assert result.data[0].district == district

    with pytest.raises(fastapi.HTTPException) as exc:
        operations.contracts.query_contract(contract_interface_stub)
    assert exc.value.status_code == 400

    with pytest.raises(fastapi.HTTPException) as exc:
        operations.contracts.query_contract(
            contract_interface_stub, winning_bidder_id=-7
        )
    assert exc.value.status_code == 404
