from fastapi import UploadFile

from mndot_bid_api.etl.extract import read_item_list_csv
from mndot_bid_api.etl.load import load_items
from mndot_bid_api.etl.transform import transform_items
from mndot_bid_api.etl.types import CSVContent
from mndot_bid_api.schema import ItemListETL


def item_list_pipeline(csv: UploadFile) -> ItemListETL:

    csv_content: CSVContent = str(csv.read())

    item_list_data = read_item_list_csv(csv_content)

    transformed_items = transform_items(item_list_data.raw_items)

    item_load_results = load_items(transformed_items)

    item_list_etl = ItemListETL(
        spec_year=item_list_data.spec_year, item_results=item_load_results
    )

    return item_list_etl
