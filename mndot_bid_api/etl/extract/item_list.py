from dataclasses import dataclass

import pandas as pd
import pandera as pa

from mndot_bid_api.etl.df_schemas import RawItems
from mndot_bid_api.etl.types import FilePathOrBuffer, RawItemsDF


@dataclass
class ItemListData:
    raw_items: RawItemsDF

    @property
    def spec_year(self) -> str:
        ...


@pa.check_output(RawItems.to_schema())
def read_item_list_csv(filepath_or_buffer: FilePathOrBuffer) -> ItemListData:
    ...
