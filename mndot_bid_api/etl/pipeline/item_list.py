import pandas as pd
import pandera as pa
from fastapi import UploadFile

from mndot_bid_api.etl.extract import read_item_list_csv
from mndot_bid_api.etl.load import load_items
from mndot_bid_api.etl.transform import transform_items
from mndot_bid_api.etl.types import CSVContent
from mndot_bid_api.operations.crud_interface import CRUDInterface
from mndot_bid_api.schema import ItemListETL


def item_list_etl_pipeline(
    csv: UploadFile, item_interface: CRUDInterface
) -> ItemListETL:

    csv_content: CSVContent = csv.read().decode()

    try:
        item_list_data = read_item_list_csv(csv_content)
        transformed_items = transform_items(
            item_list_data.raw_items, item_list_data.spec_year
        )
    except pd.errors.ParserError as exc:
        raise exc
    except pa.errors.SchemaError as exc:
        raise exc

    item_load_results = load_items(transformed_items, item_interface)

    item_list_etl = ItemListETL(
        spec_year=item_list_data.spec_year, item_results=item_load_results
    )

    return item_list_etl
