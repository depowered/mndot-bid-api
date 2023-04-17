import httpx
from fastapi import UploadFile

from mndot_bid_api import exceptions
from mndot_bid_api.etl.extract import read_abstract_csv
from mndot_bid_api.etl.load import load_bidders, load_bids, load_contract
from mndot_bid_api.etl.scrape import get_abstract_csv_path
from mndot_bid_api.etl.transform import (
    transform_bidders,
    transform_bids,
    transform_contract,
)
from mndot_bid_api.etl.types import CSVContent
from mndot_bid_api.operations.crud_interface import CRUDInterface
from mndot_bid_api.schema import AbstractETL


def abstract_etl_pipeline(
    csv: UploadFile,
    contract_interface: CRUDInterface,
    bid_interface: CRUDInterface,
    invalid_bid_interface: CRUDInterface,
    bidder_interface: CRUDInterface,
    item_interface: CRUDInterface,
) -> AbstractETL:
    try:
        csv_content: CSVContent = csv.file.read().decode()
    except UnicodeDecodeError as err:
        exceptions.raise_http_422_decode_error(err)

    try:
        abstract_data = read_abstract_csv(csv_content)

        transformed_contract = transform_contract(
            abstract_data.raw_contract, abstract_data.winning_bidder_id
        )
        transformed_bids = transform_bids(
            abstract_data.raw_bids, abstract_data.winning_bidder_id
        )
        transformed_bidders = transform_bidders(abstract_data.raw_bidders)

    except exceptions.SchemaError as err:
        exceptions.raise_http_422_schema_error(err)
    except exceptions.ParserError as err:
        exceptions.raise_http_422_parser_error(err)
    except exceptions.ParseAbstractCSVError as err:
        exceptions.raise_http_422_parser_error(err)

    contract_load_results = load_contract(transformed_contract, contract_interface)
    bid_load_results = load_bids(
        transformed_bids, bid_interface, item_interface, invalid_bid_interface
    )
    bidder_load_results = load_bidders(transformed_bidders, bidder_interface)

    abstract_etl = AbstractETL(
        contract_id=abstract_data.contract_id,
        contract_results=contract_load_results,
        bidder_results=bidder_load_results,
        bid_results=bid_load_results,
    )

    return abstract_etl


def set_etl_status_key_to_true(
    etl_id: int, update_key: str, abstract_etl_status_interface: CRUDInterface
) -> None:
    data = dict()
    data[update_key] = True
    abstract_etl_status_interface.update(etl_id, data)


def update_etl_status_on_failure(
    etl_id: int,
    failed_key: str,
    err: Exception,
    abstract_etl_status_interface: CRUDInterface,
) -> None:
    data = {
        "successful": False,
        "error_msg": err.args[0],
    }
    data[failed_key] = False
    abstract_etl_status_interface.update(etl_id, data)


async def async_abstract_etl_pipeline(
    etl_id: int,
    contract_id: int,
    abstract_etl_status_interface: CRUDInterface,
    contract_interface: CRUDInterface,
    bid_interface: CRUDInterface,
    invalid_bid_interface: CRUDInterface,
    bidder_interface: CRUDInterface,
    item_interface: CRUDInterface,
) -> None:
    # Fetch the csv file path, downloading it if it doesn't exist
    try:
        csv_file = get_abstract_csv_path(contract_id)
        set_etl_status_key_to_true(
            etl_id, "csv_downloaded", abstract_etl_status_interface
        )
    except httpx.HTTPStatusError as err:
        update_etl_status_on_failure(
            etl_id, "csv_downloaded", err, abstract_etl_status_interface
        )
        return

    # Extract abstract data
    try:
        with open(csv_file, "r") as f:
            abstract_data = read_abstract_csv(f.read())
        set_etl_status_key_to_true(etl_id, "extracted", abstract_etl_status_interface)
    except (
        exceptions.SchemaError,
        exceptions.ParserError,
        exceptions.ParseAbstractCSVError,
    ) as err:
        update_etl_status_on_failure(
            etl_id, "extracted", err, abstract_etl_status_interface
        )
        return

    # Preform transformations
    try:
        transformed_contract = transform_contract(
            abstract_data.raw_contract, abstract_data.winning_bidder_id
        )
        transformed_bids = transform_bids(
            abstract_data.raw_bids, abstract_data.winning_bidder_id
        )
        transformed_bidders = transform_bidders(abstract_data.raw_bidders)
        set_etl_status_key_to_true(etl_id, "transformed", abstract_etl_status_interface)
    except exceptions.SchemaError as err:
        update_etl_status_on_failure(
            etl_id, "transformed", err, abstract_etl_status_interface
        )
        return

    # Load Results
    _ = load_contract(transformed_contract, contract_interface)
    _ = load_bids(
        transformed_bids, bid_interface, item_interface, invalid_bid_interface
    )
    _ = load_bidders(transformed_bidders, bidder_interface)
    set_etl_status_key_to_true(etl_id, "loaded", abstract_etl_status_interface)
    set_etl_status_key_to_true(etl_id, "successful", abstract_etl_status_interface)
