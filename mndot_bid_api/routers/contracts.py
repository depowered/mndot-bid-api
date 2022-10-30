import fastapi
from mndot_bid_api import db, operations
from mndot_bid_api.operations import schema

router = fastapi.APIRouter(prefix="/contract", tags=["contract"])


@router.get(
    "/all",
    response_model=schema.ContractCollection,
    status_code=fastapi.status.HTTP_200_OK,
)
def api_read_all_contracts(
    contract_interface=fastapi.Depends(db.get_contract_interface),
) -> schema.ContractCollection:

    return operations.contracts.read_all_contracts(contract_interface)


@router.get(
    "/{contract_id}",
    response_model=schema.Contract,
    status_code=fastapi.status.HTTP_200_OK,
)
def api_read_contract(
    contract_id: int,
    contract_interface=fastapi.Depends(db.get_contract_interface),
) -> schema.Contract:

    return operations.contracts.read_contract(contract_id, contract_interface)


@router.post(
    "/",
    response_model=schema.Contract,
    status_code=fastapi.status.HTTP_201_CREATED,
)
def api_create_contract(
    data: schema.ContractCreateData,
    contract_interface=fastapi.Depends(db.get_contract_interface),
) -> schema.Contract:

    return operations.contracts.create_contract(data, contract_interface)


@router.patch(
    "/{contract_id}",
    response_model=schema.Contract,
    status_code=fastapi.status.HTTP_200_OK,
)
def api_update_contract(
    contract_id: int,
    data: schema.ContractUpdateData,
    contract_interface=fastapi.Depends(db.get_contract_interface),
) -> schema.Contract:

    return operations.contracts.update_contract(contract_id, data, contract_interface)


@router.delete(
    "/{contract_id}",
    status_code=fastapi.status.HTTP_204_NO_CONTENT,
)
def api_delete_contract(
    contract_id: int,
    contract_interface=fastapi.Depends(db.get_contract_interface),
):

    return operations.contracts.delete_contract(contract_id, contract_interface)
