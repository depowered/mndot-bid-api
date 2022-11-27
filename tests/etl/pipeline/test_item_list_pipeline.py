import pandas as pd
import pytest

from mndot_bid_api.db import models
from mndot_bid_api.db.interface import DBModelInterface
from mndot_bid_api.etl.pipeline.item_list import item_list_etl_pipeline


def test_item_list_etl_pipeline(item_list_csv_file, configured_sessionmaker):
    item_interface = DBModelInterface(models.Item, configured_sessionmaker)
    item_list_etl = item_list_etl_pipeline(item_list_csv_file, item_interface)

    assert item_list_etl.spec_year == "2018"
    assert len(item_list_etl.item_results) == 8032


def test_item_list_etl_pipeline_raises(abstract_csv_file, configured_sessionmaker):
    item_interface = DBModelInterface(models.Item, configured_sessionmaker)
    with pytest.raises(pd.errors.ParserError):
        item_list_etl_pipeline(abstract_csv_file, item_interface)
