import fastapi
from mndot_bid_api import operations
from mndot_bid_api.db import database
from mndot_bid_api.operations import schema
from sqlalchemy.orm import Session

router = fastapi.APIRouter(prefix="/contract", tags=["contract"])


@router.get(
    "/all",
    response_model=schema.ContractCollection,
    status_code=fastapi.status.HTTP_200_OK,
)
def api_read_all_contracts(
    db: Session = fastapi.Depends(database.get_db_session),
) -> schema.ContractCollection:

    return operations.contracts.read_all_contracts(db)


@router.get(
    "/{contract_id}",
    response_model=schema.Contract,
    status_code=fastapi.status.HTTP_200_OK,
)
def api_read_contract(
    contract_id: int, db: Session = fastapi.Depends(database.get_db_session)
) -> schema.Contract:

    return operations.contracts.read_contract(contract_id, db)


@router.post(
    "/",
    response_model=schema.Contract,
    status_code=fastapi.status.HTTP_201_CREATED,
)
def api_create_contract(
    data: schema.ContractCreateData,
    db: Session = fastapi.Depends(database.get_db_session),
) -> schema.Contract:

    return operations.contracts.create_contract(data, db)


@router.patch(
    "/{contract_id}",
    response_model=schema.Contract,
    status_code=fastapi.status.HTTP_200_OK,
)
def api_update_contract(
    contract_id: int,
    data: schema.ContractUpdateData,
    db: Session = fastapi.Depends(database.get_db_session),
) -> schema.Contract:

    return operations.contracts.update_contract(contract_id, data, db)


@router.delete(
    "/{contract_id}",
    status_code=fastapi.status.HTTP_204_NO_CONTENT,
)
def api_delete_contract(
    contract_id: int,
    db: Session = fastapi.Depends(database.get_db_session),
):

    return operations.contracts.delete_contract(contract_id, db)
