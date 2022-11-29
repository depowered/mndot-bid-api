from datetime import date

from sqlalchemy.orm import sessionmaker

from mndot_bid_api import enums, schema
from mndot_bid_api.db import models
from mndot_bid_api.db.interface import DBModelInterface
from mndot_bid_api.etl.extract.abstract import read_abstract_csv
from mndot_bid_api.etl.load.contract import load_contract
from mndot_bid_api.etl.transform.contract import transform_contract


def test_load_contract(
    abstract_csv_content: str, configured_sessionmaker: sessionmaker
):
    # Setup CRUD Interface
    model = models.Contract
    interface = DBModelInterface(model, configured_sessionmaker)

    # Extract and transform data
    abstract_data = read_abstract_csv(abstract_csv_content)
    transformed_df = transform_contract(
        abstract_data.raw_contract, abstract_data.winning_bidder_id
    )

    # Expected result when record already exists
    input_data = schema.ContractCreateData(
        id=220005,
        letting_date=date(year=2022, month=1, day=28),
        sp_number="5625-20",
        district=enums.District.DETROIT_LAKES,
        county=enums.County.OTTER_TAIL,
        description="LOCATED ON T.H. 108 FROM 420' WEST OF EB T.H. 94 RAMP TO 9TH ST NW.",
        winning_bidder_id=207897,
    )
    already_exists_load_result = schema.ContractLoadResult(
        model="Contract",
        operation="create",
        status_code=303,
        input_data=input_data,
        message="Contract already exists at ID 220005",
    )

    # Load the data
    load_results = load_contract(transformed_df, interface)

    assert len(load_results) == 1
    first_load_result = load_results[0]
    assert first_load_result == already_exists_load_result

    # Expected load result when record doesn't already exist
    record_data = schema.Contract(data=schema.ContractResult(**input_data.dict()))
    new_record_load_result = schema.ContractLoadResult(
        model="Contract",
        operation="create",
        status_code=201,
        input_data=input_data,
        record_data=record_data,
    )

    # Delete the record and reload the data
    interface.delete(220005)
    load_results = load_contract(transformed_df, interface)

    assert len(load_results) == 1
    first_load_result = load_results[0]
    assert first_load_result == new_record_load_result
