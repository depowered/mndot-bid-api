from fastapi import UploadFile

from mndot_bid_api import exceptions
from mndot_bid_api.etl.extract import read_abstract_csv
from mndot_bid_api.etl.load import load_bidders, load_bids, load_contract
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
        csv_content: CSVContent = csv.read().decode()
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
