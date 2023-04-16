from typing import Any

import pandera as pa

from mndot_bid_api import exceptions
from mndot_bid_api.etl.df_schemas import TransformedBidders
from mndot_bid_api.etl.types import TransformedBiddersDF
from mndot_bid_api.operations.bidders import create_bidder
from mndot_bid_api.operations.crud_interface import CRUDInterface
from mndot_bid_api.schema import BidderCreateData, BidderLoadResult


@pa.check_io(transformed_bidders=TransformedBidders.to_schema())
def load_bidders(
    transformed_bidders: TransformedBiddersDF, bidder_interface: CRUDInterface
) -> list[BidderLoadResult]:
    entries: list[dict[str, Any]] = [
        row._asdict()
        for row in transformed_bidders.itertuples(index=False, name="Bidder")
    ]

    load_results = []

    for entry in entries:
        create_data = BidderCreateData(**entry)
        load_result = BidderLoadResult(
            model="Bidder", operation="create", input_data=create_data
        )
        try:
            create_result = create_bidder(create_data, bidder_interface)
            load_result.status_code = 201
            load_result.record_data = create_result
        except exceptions.HTTPException as exc:
            load_result.status_code = exc.status_code
            load_result.message = exc.detail

        load_results.append(load_result)

    return load_results


@pa.check_io(transformed_bidders=TransformedBidders.to_schema())
def load_bidders_quiet(
    transformed_bidders: TransformedBiddersDF, bidder_interface: CRUDInterface
) -> None:
    entries: list[dict[str, Any]] = [
        row._asdict()
        for row in transformed_bidders.itertuples(index=False, name="Bidder")
    ]

    for entry in entries:
        create_data = BidderCreateData(**entry)
        try:
            _ = create_bidder(create_data, bidder_interface)
        except exceptions.HTTPException:
            pass  # TODO Add logging
