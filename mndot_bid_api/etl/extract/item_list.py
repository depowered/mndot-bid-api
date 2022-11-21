from dataclasses import dataclass
from io import StringIO

import pandas as pd

from mndot_bid_api.etl.df_schemas import RawItems
from mndot_bid_api.etl.types import CSVContent, RawItemsDF


@dataclass
class ItemListData:
    raw_items: RawItemsDF

    @property
    def spec_year(self) -> str:
        return "20" + self.raw_items.at[0, "Spec Year"]


def read_item_list_csv(csv_content: CSVContent) -> ItemListData:
    df = pd.read_csv(StringIO(csv_content), dtype=pd.StringDtype.name, quotechar="'")
    validated_df = RawItems.validate(df)
    return ItemListData(validated_df)
