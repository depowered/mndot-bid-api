import fastapi

from mndot_bid_api import exceptions, schema
from mndot_bid_api.etl.pipeline.abstract import async_abstract_etl_pipeline
from mndot_bid_api.operations.crud_interface import CRUDInterface


def read_abstract_etl_status(
    etl_id: int, abstract_etl_status_interface: CRUDInterface
) -> schema.AbstractETLStatusResult:
    try:
        record = abstract_etl_status_interface.read_by_id(etl_id)

    except exceptions.RecordNotFoundError as exc:
        exceptions.raise_http_404(model_name="AbstractETLStatus", id=etl_id, exc=exc)

    result = schema.AbstractETLStatusResult(**record)

    return result


def dispatch_abstract_etl(
    contract_id: int,
    background_tasks: fastapi.BackgroundTasks,
    abstract_etl_status_interface: CRUDInterface,
    contract_interface: CRUDInterface,
    bid_interface: CRUDInterface,
    invalid_bid_interface: CRUDInterface,
    bidder_interface: CRUDInterface,
    item_interface: CRUDInterface,
) -> schema.AbstractETLStatusResult:
    # Create initial status record
    etl_status = abstract_etl_status_interface.create(data={"contract_id": contract_id})

    # Dispatch pipeline process
    background_tasks.add_task(
        func=async_abstract_etl_pipeline,
        etl_id=etl_status["id"],
        contract_id=contract_id,
        abstract_etl_status_interface=abstract_etl_status_interface,
        contract_interface=contract_interface,
        bid_interface=bid_interface,
        invalid_bid_interface=invalid_bid_interface,
        bidder_interface=bidder_interface,
        item_interface=item_interface,
    )

    return schema.AbstractETLStatusResult(**etl_status)
