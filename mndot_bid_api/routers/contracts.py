from fastapi import APIRouter

from mndot_bid_api.operations.contracts import read_all_contracts, read_contract


router = APIRouter()


@router.get("/contracts")
def api_read_all_contracts():
    return read_all_contracts()


@router.get("/contract/{contract_id}")
def api_read_contract(contract_id):
    return read_contract(contract_id)
