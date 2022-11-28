from fastapi import UploadFile

from mndot_bid_api import exceptions
from mndot_bid_api.etl.extract import read_item_list_csv
from mndot_bid_api.etl.load import load_items
from mndot_bid_api.etl.transform import transform_items
from mndot_bid_api.etl.types import CSVContent
from mndot_bid_api.operations.crud_interface import CRUDInterface
from mndot_bid_api.schema import ItemListETL


def item_list_etl_pipeline(
    csv: UploadFile, item_interface: CRUDInterface
) -> ItemListETL:

    try:
        csv_content: CSVContent = csv.file.read().decode()
    except UnicodeDecodeError as err:
        exceptions.raise_http_422_decode_error(err)

    try:
        item_list_data = read_item_list_csv(csv_content)
        transformed_items = transform_items(
            item_list_data.raw_items, item_list_data.spec_year
        )
    except exceptions.ParserError as err:
        exceptions.raise_http_422_parser_error(err)
    except exceptions.SchemaError as err:
        exceptions.raise_http_422_schema_error(err)

    item_load_results = load_items(transformed_items, item_interface)

    item_list_etl = ItemListETL(
        spec_year=item_list_data.spec_year, item_results=item_load_results
    )

    return item_list_etl
