from sqlalchemy import select

from mndot_bid_api.db.engine import DBSession
from mndot_bid_api.db.models import DBContract, to_dict
from mndot_bid_api.operations.models import ContractResult


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
