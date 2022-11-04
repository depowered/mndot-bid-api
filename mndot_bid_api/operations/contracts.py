import fastapi
from mndot_bid_api.exceptions import (
    RecordAlreadyExistsException,
    RecordNotFoundException,
)
from mndot_bid_api.operations import schema
from mndot_bid_api.operations.crud_interface import CRUDInterface


def read_all_contracts(contract_interface: CRUDInterface) -> schema.ContractCollection:
    records = contract_interface.read_all()

    results = [schema.ContractResult(**record) for record in records]

    return schema.ContractCollection(data=results)


def read_contract(
    contract_id: int, contract_interface: CRUDInterface
) -> schema.Contract:
    try:
        record = contract_interface.read_by_id(contract_id)

    except RecordNotFoundException as exc:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_404_NOT_FOUND,
            detail=f"Contract at ID {contract_id} not found",
        ) from exc

    result = schema.ContractResult(**record)

    return schema.Contract(data=result)


def create_contract(
    data: schema.ContractCreateData, contract_interface: CRUDInterface
) -> schema.Contract:
    try:
        record = contract_interface.create(data.dict())

    except RecordAlreadyExistsException as exc:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_303_SEE_OTHER,
            detail=f"Contract already exists at ID {data.id}",
        ) from exc

    result = schema.ContractResult(**record)

    return schema.Contract(data=result)


def update_contract(
    contract_id: int, data: schema.ContractUpdateData, contract_interface: CRUDInterface
) -> schema.Contract:
    try:
        record = contract_interface.update(
            id=contract_id, data=data.dict(exclude_none=True)
        )

    except RecordNotFoundException as exc:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_404_NOT_FOUND,
            detail=f"Contract at ID {contract_id} not found",
        ) from exc

    result = schema.ContractResult(**record)

    return schema.Contract(data=result)


def delete_contract(contract_id: int, contract_interface: CRUDInterface) -> None:
    try:
        contract_interface.delete(contract_id)

    except RecordNotFoundException as exc:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_404_NOT_FOUND,
            detail=f"Contract at ID {contract_id} not found",
        ) from exc


def query_contract(
    contract_interface: CRUDInterface, **kwargs
) -> schema.ContractCollection:
    if not kwargs:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_400_BAD_REQUEST,
            detail=f"Provide at least one query parameter",
        )

    try:
        records = contract_interface.read_all_by_kwargs(**kwargs)

    except RecordNotFoundException as exc:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_404_NOT_FOUND,
            detail=f"No Contracts found matching the provided query parameters",
        ) from exc

    results = [schema.ContractResult(**record) for record in records]

    return schema.ContractCollection(data=results)
