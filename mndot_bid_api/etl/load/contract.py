from typing import Any

import pandera as pa

from mndot_bid_api import exceptions
from mndot_bid_api.etl.df_schemas import TransformedContract
from mndot_bid_api.etl.types import TransformedContractDF
from mndot_bid_api.operations.contracts import create_contract
from mndot_bid_api.operations.crud_interface import CRUDInterface
from mndot_bid_api.schema import ContractCreateData, ContractLoadResult


@pa.check_io(transformed_contract=TransformedContract.to_schema())
def load_contract(
    transformed_contract: TransformedContractDF, contract_interface: CRUDInterface
) -> list[ContractLoadResult]:

    entries: list[dict[str, Any]] = [
        row._asdict()
        for row in transformed_contract.itertuples(index=False, name="Contract")
    ]

    load_results = []

    for entry in entries:
        create_data = ContractCreateData(**entry)
        load_result = ContractLoadResult(
            model="Contract", operation="create", input_data=create_data
        )
        try:
            create_result = create_contract(create_data, contract_interface)
            load_result.status_code = 201
            load_result.record_data = create_result
        except exceptions.HTTPException as exc:
            load_result.status_code = exc.status_code
            load_result.message = exc.detail

        load_results.append(load_result)

    return load_results
