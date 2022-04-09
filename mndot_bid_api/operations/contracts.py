from sqlalchemy import select

from mndot_bid_api.db.engine import DBSession
from mndot_bid_api.db.models import DBContract, to_dict
from mndot_bid_api.operations.models import (
    ContractCreateData,
    ContractResult,
    ContractUpdateData,
)


def read_all_contracts() -> list[ContractResult]:
    with DBSession() as session:
        statement = select(DBContract)
        contracts: list[DBContract] = session.execute(statement).scalars().all()
        return [ContractResult(**to_dict(c)) for c in contracts]


def read_contract(contract_id: int) -> ContractResult:
    with DBSession() as session:
        contract = session.get(DBContract, contract_id)
        if not contract:
            return {"message": f"Contract with ID {contract_id} not found."}
        return ContractResult(**to_dict(contract))


def create_contract(data: ContractCreateData) -> ContractResult:
    with DBSession() as session:
        contract = DBContract(**data.dict())

        # verify that contract is not already in the database before adding
        in_db = session.get(DBContract, contract.id)
        if in_db:
            return {
                "message": f"Contract with ID {contract.id} already exists in the database."
            }

        session.add(contract)
        session.commit()
        return ContractResult(**to_dict(contract))


def update_contract(contract_id: int, data: ContractUpdateData) -> ContractResult:
    with DBSession() as session:
        contract: DBContract = session.get(DBContract, contract_id)
        for key, value in data.dict(exclude_none=True).items():
            setattr(contract, key, value)

        session.commit()
        return ContractResult(**to_dict(contract))
