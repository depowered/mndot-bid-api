from fastapi import HTTPException
from mndot_bid_api.db.database import DBSession
from mndot_bid_api.db.models import Contract, to_dict
from mndot_bid_api.operations.models import (
    ContractCreateData,
    ContractResult,
    ContractUpdateData,
)
from sqlalchemy import select


def read_all_contracts() -> list[ContractResult]:
    with DBSession() as session:
        statement = select(Contract)
        contracts: list[Contract] = session.execute(statement).scalars().all()
        return [ContractResult(**to_dict(c)) for c in contracts]


def read_contract(contract_id: int) -> ContractResult:
    with DBSession() as session:
        contract = session.get(Contract, contract_id)
        if not contract:
            return {"message": f"Contract with ID {contract_id} not found."}
        return ContractResult(**to_dict(contract))


def create_contract(data: ContractCreateData) -> ContractResult:
    with DBSession() as session:
        contract = Contract(**data.dict())

        # verify that contract is not already in the database before adding
        selected_contract = session.get(Contract, contract.id)
        if selected_contract:
            raise HTTPException(
                status_code=303,
                detail=f"Contract already exists at ID {selected_contract.id}.",
            )

        session.add(contract)
        session.commit()
        return ContractResult(**to_dict(contract))


def update_contract(contract_id: int, data: ContractUpdateData) -> ContractResult:
    with DBSession() as session:
        contract: Contract = session.get(Contract, contract_id)

        if not contract:
            raise HTTPException(
                status_code=404, detail=f"Contract with ID {contract_id} not found."
            )

        for key, value in data.dict(exclude_none=True).items():
            setattr(contract, key, value)

        session.commit()
        return ContractResult(**to_dict(contract))
