from dataclasses import dataclass
from io import StringIO

import pandas as pd
import pandera as pa

from mndot_bid_api.etl.df_schemas import RawItems
from mndot_bid_api.etl.types import CSVContent, RawItemsDF


@dataclass
class ItemListData:
    raw_items: RawItemsDF

    @property
    def spec_year(self) -> str:
        return "20" + self.raw_items.at[0, "Spec Year"]


def read_item_list_csv(csv_content: CSVContent) -> ItemListData:
    try:
        df = pd.read_csv(StringIO(csv_content), dtype=str, quotechar="'")
        validated_df = RawItems.validate(df)
    except pd.errors.ParserError as exc:
        raise exc
    except pa.errors.SchemaError as exc:
        raise exc

    return ItemListData(validated_df)
