from datetime import date

import fastapi

from mndot_bid_api import auth, db, operations, schema

contract_router = fastapi.APIRouter(prefix="/contract", tags=["contract"])


@contract_router.get(
    "/all",
    response_model=schema.ContractCollection,
    status_code=fastapi.status.HTTP_200_OK,
)
def api_read_all_contracts(
    limit: int = 100,
    contract_interface=fastapi.Depends(db.get_contract_interface),
) -> schema.ContractCollection:

    return operations.contracts.read_all_contracts(limit, contract_interface)


@contract_router.get(
    "/{contract_id}",
    response_model=schema.Contract,
    status_code=fastapi.status.HTTP_200_OK,
)
def api_read_contract(
    contract_id: int,
    contract_interface=fastapi.Depends(db.get_contract_interface),
) -> schema.Contract:

    return operations.contracts.read_contract(contract_id, contract_interface)


@contract_router.post(
    "/",
    response_model=schema.Contract,
    status_code=fastapi.status.HTTP_201_CREATED,
)
def api_create_contract(
    data: schema.ContractCreateData,
    contract_interface=fastapi.Depends(db.get_contract_interface),
    api_key: auth.APIKeyHeader = fastapi.Depends(auth.authorize_api_key),
) -> schema.Contract:

    return operations.contracts.create_contract(data, contract_interface)


@contract_router.patch(
    "/{contract_id}",
    response_model=schema.Contract,
    status_code=fastapi.status.HTTP_200_OK,
)
def api_update_contract(
    contract_id: int,
    data: schema.ContractUpdateData,
    contract_interface=fastapi.Depends(db.get_contract_interface),
    api_key: auth.APIKeyHeader = fastapi.Depends(auth.authorize_api_key),
) -> schema.Contract:

    return operations.contracts.update_contract(contract_id, data, contract_interface)


@contract_router.delete(
    "/{contract_id}",
    status_code=fastapi.status.HTTP_204_NO_CONTENT,
)
def api_delete_contract(
    contract_id: int,
    contract_interface=fastapi.Depends(db.get_contract_interface),
    api_key: auth.APIKeyHeader = fastapi.Depends(auth.authorize_api_key),
):

    return operations.contracts.delete_contract(contract_id, contract_interface)


@contract_router.get(
    "/query/",
    response_model=schema.ContractCollection,
    status_code=fastapi.status.HTTP_200_OK,
)
def api_query_contract(
    letting_date: date | None = None,
    sp_number: str | None = None,
    district: str | None = None,
    county: str | None = None,
    description: str | None = None,
    winning_bidder_id: int | None = None,
    contract_interface=fastapi.Depends(db.get_contract_interface),
    limit: int = 100,
) -> schema.ContractCollection:
    kwargs = locals()

    # Filter for non-None keyword arguments to pass to the query function
    filtered_kwargs = {
        key: value
        for key, value in kwargs.items()
        if value and key not in ["contract_interface", "limit"]
    }

    return operations.contracts.query_contract(
        contract_interface, limit, **filtered_kwargs
    )
