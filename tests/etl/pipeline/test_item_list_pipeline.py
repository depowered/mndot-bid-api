import io

import fastapi
import pytest

from mndot_bid_api import exceptions
from mndot_bid_api.db import models
from mndot_bid_api.db.interface import DBModelInterface
from mndot_bid_api.etl.pipeline.item_list import item_list_etl_pipeline


@pytest.mark.skipif(
    "not config.getoption('--run-slow')",
    reason="Only run when --run-slow is given",
)
def test_item_list_etl_pipeline(item_list_csv_file, configured_sessionmaker):
    item_interface = DBModelInterface(models.Item, configured_sessionmaker)
    item_list_etl = item_list_etl_pipeline(item_list_csv_file, item_interface)

    assert item_list_etl.spec_year == "2018"
    assert len(item_list_etl.item_results) == 8032


def test_item_list_etl_pipeline_raises(abstract_csv_file, configured_sessionmaker):
    item_interface = DBModelInterface(models.Item, configured_sessionmaker)
    with pytest.raises(exceptions.HTTPException):
        item_list_etl_pipeline(abstract_csv_file, item_interface)

    with pytest.raises(exceptions.HTTPException) as err:
        with open(
            "./tests/data/not_a_valid_csv.jpg", "rb", io.DEFAULT_BUFFER_SIZE
        ) as f:
            invalid_csv = fastapi.UploadFile(filename="invalid.csv", file=f)
            item_list_etl_pipeline(invalid_csv, item_interface)
    assert err.value.detail["error"] == "UnicodeDecodeError"
