from mndot_bid_api import exceptions, schema
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

    except exceptions.RecordNotFoundError as exc:
        exceptions.raise_http_404(model_name="Contract", id=contract_id, exc=exc)

    result = schema.ContractResult(**record)

    return schema.Contract(data=result)


def create_contract(
    data: schema.ContractCreateData, contract_interface: CRUDInterface
) -> schema.Contract:
    try:
        record = contract_interface.create(data.dict())

    except exceptions.RecordAlreadyExistsError as exc:
        contract_id = exc.args[0]["id"]
        exceptions.raise_http_303(model_name="Contract", id=contract_id, exc=exc)

    result = schema.ContractResult(**record)

    return schema.Contract(data=result)


def update_contract(
    contract_id: int, data: schema.ContractUpdateData, contract_interface: CRUDInterface
) -> schema.Contract:
    try:
        record = contract_interface.update(
            id=contract_id, data=data.dict(exclude_none=True)
        )

    except exceptions.RecordNotFoundError as exc:
        exceptions.raise_http_404(model_name="Contract", id=contract_id, exc=exc)

    result = schema.ContractResult(**record)

    return schema.Contract(data=result)


def delete_contract(contract_id: int, contract_interface: CRUDInterface) -> None:
    try:
        contract_interface.delete(contract_id)

    except exceptions.RecordNotFoundError as exc:
        exceptions.raise_http_404(model_name="Contract", id=contract_id, exc=exc)


def query_contract(
    contract_interface: CRUDInterface, **kwargs
) -> schema.ContractCollection:
    if not kwargs:
        exceptions.raise_http_400_empty_query()

    try:
        records = contract_interface.read_all_by_kwargs(**kwargs)

    except exceptions.RecordNotFoundError as exc:
        exceptions.raise_http_404_query(model_name="Contract", exc=exc)

    results = [schema.ContractResult(**record) for record in records]

    return schema.ContractCollection(data=results)
