from typing import List
from fastapi import APIRouter

from mndot_bid_api.operations.contracts import (
    create_contract,
    read_all_contracts,
    read_contract,
    update_contract,
)
from mndot_bid_api.operations.models import (
    ContractCreateData,
    ContractResult,
    ContractUpdateData,
)


router = APIRouter()


@router.get("/contracts", tags=["contracts"], response_model=List[ContractResult])
def api_read_all_contracts() -> List[ContractResult]:
    return read_all_contracts()


@router.get(
    "/contract/{contract_id}", tags=["contracts"], response_model=ContractResult
)
def api_read_contract(contract_id) -> ContractResult:
    return read_contract(contract_id)


@router.post("/contract", tags=["contracts"], response_model=ContractResult)
def api_create_contract(contract: ContractCreateData) -> ContractResult:
    return create_contract(contract)


@router.patch(
    "/contract/{contract_id}", tags=["contracts"], response_model=ContractResult
)
def api_update_contract(
    contract_id: int, contract: ContractUpdateData
) -> ContractResult:
    return update_contract(contract_id, contract)
