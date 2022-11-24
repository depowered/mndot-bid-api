from sqlalchemy.orm import sessionmaker

from mndot_bid_api import schema
from mndot_bid_api.db import models
from mndot_bid_api.db.interface import DBModelInterface
from mndot_bid_api.etl.extract.abstract import read_abstract_csv
from mndot_bid_api.etl.load.bidders import load_bidders
from mndot_bid_api.etl.transform.bidders import transform_bidders


def test_load_bidders(abstract_csv_content: str, configured_sessionmaker: sessionmaker):
    # Setup CRUD Interface
    model = models.Bidder
    interface = DBModelInterface(model, configured_sessionmaker)

    # Extract and transform data
    abstract_data = read_abstract_csv(abstract_csv_content)
    transformed_df = transform_bidders(abstract_data.raw_bidders)

    # Expected result when record already exists
    input_data = schema.BidderCreateData(id=207897, name="Central Specialties, Inc.")
    record_data = schema.Bidder(data=schema.BidderResult(**input_data.dict()))
    already_exists_load_result = schema.LoadResult(
        model="Bidder",
        operation="create",
        status_code=303,
        input_data=input_data,
        message="Bidder already exists at ID 207897",
    )

    # Load the data
    load_results = load_bidders(transformed_df, interface)

    assert len(load_results) == 3
    first_load_result = load_results[0]
    assert first_load_result == already_exists_load_result

    # Expected load result when record doesn't already exist
    record_data = schema.Bidder(data=schema.BidderResult(**input_data.dict()))
    new_record_load_result = schema.LoadResult(
        model="Bidder",
        operation="create",
        status_code=201,
        input_data=input_data,
        record_data=record_data,
    )

    # Delete the record and reload the data
    interface.delete(207897)
    load_results = load_bidders(transformed_df, interface)

    assert len(load_results) == 3
    first_load_result = load_results[0]
    assert first_load_result == new_record_load_result
