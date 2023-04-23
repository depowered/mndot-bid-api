from pathlib import Path

import fastapi
import httpx

from mndot_bid_api import exceptions, schema
from mndot_bid_api.core.config import CSV_DIR
from mndot_bid_api.etl.pipeline.abstract import async_abstract_etl_pipeline
from mndot_bid_api.etl.scrape.abstract import (download_abstract_to_csv_dir,
                                               scrape_contract_ids)
from mndot_bid_api.operations.crud_interface import CRUDInterface


def read_abstract_etl_status(
    etl_id: int, abstract_etl_status_interface: CRUDInterface
) -> schema.AbstractETLResult:
    try:
        record = abstract_etl_status_interface.read_by_id(etl_id)

    except exceptions.RecordNotFoundError as exc:
        exceptions.raise_http_404(model_name="AbstractETL", id=etl_id, exc=exc)

    result = schema.AbstractETLResult(**record)

    return result


def dispatch_abstract_etl(
    contract_id: int,
    background_tasks: fastapi.BackgroundTasks,
    abstract_etl_interface: CRUDInterface,
    contract_interface: CRUDInterface,
    bid_interface: CRUDInterface,
    invalid_bid_interface: CRUDInterface,
    bidder_interface: CRUDInterface,
    item_interface: CRUDInterface,
) -> schema.DispatchAbstractETL:
    # Create initial abstract etl record
    create_data = schema.AbstractELTCreateData(contract_id=contract_id)
    record = abstract_etl_interface.create(create_data.dict())

    # Dispatch pipeline process
    background_tasks.add_task(
        func=async_abstract_etl_pipeline,
        etl_id=record["id"],
        contract_id=contract_id,
        abstract_etl_interface=abstract_etl_interface,
        contract_interface=contract_interface,
        bid_interface=bid_interface,
        invalid_bid_interface=invalid_bid_interface,
        bidder_interface=bidder_interface,
        item_interface=item_interface,
    )

    return schema.DispatchAbstractETL(etl_id=record["id"], contract_id=contract_id)


def scrape_abstracts(year: int) -> schema.ScrapeAbstractResult:
    # Scrape a list of contract ids
    scraped_contract_ids = set(scrape_contract_ids(year))

    # Get a list of all csvs in the in the CSV_DIR
    csv_dir_path = Path(CSV_DIR)
    existing_contract_ids = {int(f.stem) for f in csv_dir_path.glob("*.csv")}

    # Download the missing csvs
    new_contract_ids = scraped_contract_ids - existing_contract_ids
    abstracts_downloaded = []
    failed_to_download = []
    for contract_id in new_contract_ids:
        file_path = csv_dir_path / f"{contract_id}.csv"
        try:
            download_abstract_to_csv_dir(contract_id)
            abstracts_downloaded.append(contract_id)
        except httpx.HTTPStatusError:
            failed_to_download.append(contract_id)

    # Return the scrape result
    return schema.ScrapeAbstractResult(
        year=year,
        total_abstract_count=len(scraped_contract_ids),
        new_count=len(new_contract_ids),
        abstracts_downloaded=sorted(abstracts_downloaded),
        failed_to_download=sorted(failed_to_download),
    )
