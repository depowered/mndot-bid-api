from fastapi import APIRouter

from mndot_bid_api.operations.contracts import (
    create_contract,
    read_all_contracts,
    read_contract,
    update_contract,
)
from mndot_bid_api.operations.models import (
    BidderResult,
    ContractCreateData,
    ContractResult,
    ContractUpdateData,
)


router = APIRouter()


@router.get("/contracts", tags=["contracts"])
def api_read_all_contracts():
    return read_all_contracts()


@router.get("/contract/{contract_id}", tags=["contracts"])
def api_read_contract(contract_id):
    return read_contract(contract_id)


@router.post("/contract", tags=["contracts"])
def api_create_contract(contract: ContractCreateData) -> ContractResult:
    return create_contract(contract)


@router.patch("/contract/{contract_id}", tags=["contracts"])
def api_update_contract(contract_id: int, contract: ContractUpdateData) -> BidderResult:
    return update_contract(contract_id, contract)
