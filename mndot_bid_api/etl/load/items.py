from typing import Any

import pandera as pa

from mndot_bid_api import exceptions
from mndot_bid_api.etl.df_schemas import TransformedItems
from mndot_bid_api.etl.types import TransformedItemsDF
from mndot_bid_api.operations.crud_interface import CRUDInterface
from mndot_bid_api.operations.items import create_item, update_item
from mndot_bid_api.schema import ItemCreateData, ItemLoadResult, ItemUpdateData


@pa.check_input(TransformedItems.to_schema())
def load_items(
    transformed_items: TransformedItemsDF, item_interface: CRUDInterface
) -> list[ItemLoadResult]:

    entries: list[dict[str, Any]] = [
        row._asdict() for row in transformed_items.itertuples(index=False, name="Item")
    ]

    load_results = []

    for entry in entries:
        create_data = ItemCreateData(**entry)
        load_result = ItemLoadResult(
            model="Item", operation="create", input_data=create_data
        )
        try:
            create_result = create_item(create_data, item_interface)
            load_result.status_code = 201
            load_result.record_data = create_result
        except exceptions.HTTPException as exc:
            load_result.operation = "update"
            load_result.message = f"{exc.detail} Redirect to update item."
            try:
                item_id = int(exc.detail.split(" ")[-1])
                update_data = ItemUpdateData(**create_data.dict())
                update_result = update_item(item_id, update_data, item_interface)
                load_result.status_code = 200
                load_result.record_data = update_result
            except exceptions.HTTPException as err:
                load_result.status_code = err.status_code
                load_result.message += f" {err.detail}"

        load_results.append(load_result)

    return load_results
