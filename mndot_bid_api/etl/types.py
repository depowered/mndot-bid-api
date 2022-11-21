from typing import Callable

import pandera as pa
from pandas._typing import FilePath, ReadCsvBuffer

from mndot_bid_api import schema
from mndot_bid_api.etl import df_schemas

############################################################################

CSVBuffer = FilePath | ReadCsvBuffer[bytes] | ReadCsvBuffer[str]

############################################################################

RawBiddersDF = pa.typing.DataFrame[df_schemas.RawBidders]
RawBidsDF = pa.typing.DataFrame[df_schemas.RawBids]
RawContractDF = pa.typing.DataFrame[df_schemas.RawContract]
RawItemsDF = pa.typing.DataFrame[df_schemas.RawItems]

RawEntitiesDF = RawBiddersDF | RawBidsDF | RawContractDF | RawItemsDF

ExtractFunction = Callable[[CSVBuffer], RawEntitiesDF]

############################################################################

TransformedBiddersDF = pa.typing.DataFrame[df_schemas.TransformedBidders]
TransformedBidsDF = pa.typing.DataFrame[df_schemas.TransformedBids]
TransformedContractDF = pa.typing.DataFrame[df_schemas.TransformedContract]
TransformedItemsDF = pa.typing.DataFrame[df_schemas.TransformedItems]

TransformedEntitiesDF = (
    TransformedBiddersDF
    | TransformedBidsDF
    | TransformedContractDF
    | TransformedItemsDF
)

TransformFunction = Callable[[RawEntitiesDF], TransformedEntitiesDF]

############################################################################

LoadResults = list[schema.LoadResult]

LoadFunction = Callable[[TransformedEntitiesDF], LoadResults]
