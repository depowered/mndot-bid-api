from typing import Any

import pandera as pa

from mndot_bid_api import exceptions
from mndot_bid_api.etl.df_schemas import TransformedBids
from mndot_bid_api.etl.types import TransformedBidsDF
from mndot_bid_api.operations.bids import create_bid
from mndot_bid_api.operations.crud_interface import CRUDInterface
from mndot_bid_api.operations.invalid_bids import create_invalid_bid
from mndot_bid_api.schema import BidCreateData, BidLoadResult


@pa.check_io(transformed_bids=TransformedBids.to_schema())
def load_bids(
    transformed_bids: TransformedBidsDF,
    bid_interface: CRUDInterface,
    item_interface: CRUDInterface,
    invalid_bid_interface: CRUDInterface,
) -> list[BidLoadResult]:

    entries: list[dict[str, Any]] = [
        row._asdict() for row in transformed_bids.itertuples(index=False, name="Bid")
    ]

    load_results = []

    for entry in entries:
        create_data = BidCreateData(**entry)
        load_result = BidLoadResult(
            model="Bid", operation="create", input_data=create_data
        )
        try:
            create_result = create_bid(create_data, bid_interface, item_interface)
            load_result.status_code = 201
            load_result.record_data = create_result
        except exceptions.HTTPException as exc:
            load_result.status_code = exc.status_code
            load_result.message = exc.detail
        except exceptions.InvalidBidError as err:
            load_result.model = "InvalidBid"
            load_result.message = err.args[0]
            try:
                create_result = create_invalid_bid(create_data, invalid_bid_interface)
                load_result.status_code = 201
                load_result.record_data = create_result
            except exceptions.HTTPException as exc:
                load_result.status_code = exc.status_code
                load_result.message += f" {exc.detail}"

        load_results.append(load_result)

    return load_results
