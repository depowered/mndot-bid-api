from mndot_bid_api.etl.extract import read_abstract_csv
from mndot_bid_api.etl.load import load_bidders, load_bids, load_contract
from mndot_bid_api.etl.transform import (
    transform_bidders,
    transform_bids,
    transform_contract,
)
from mndot_bid_api.etl.types import CSVBuffer
from mndot_bid_api.schema import AbstractETL


def abstract_pipeline(filepath_or_buffer: CSVBuffer) -> AbstractETL:

    abstract_data = read_abstract_csv(filepath_or_buffer)

    transformed_bidders = transform_bidders(abstract_data.raw_bidders)
    bidder_load_results = load_bidders(transformed_bidders)

    transformed_bids = transform_bids(abstract_data.raw_bids)
    bid_load_results = load_bids(transformed_bids)

    transformed_contract = transform_contract(abstract_data.raw_contract)
    contract_load_results = load_contract(transformed_contract)

    abstract_etl = AbstractETL(
        contract_id=abstract_data.contract_id,
        contract_results=contract_load_results,
        bidder_results=bidder_load_results,
        bid_results=bid_load_results,
    )

    return abstract_etl
