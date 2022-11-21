from typing import Callable

from pandera.typing import DataFrame

from mndot_bid_api import schema
from mndot_bid_api.etl.df_schemas import (
    RawBidders,
    RawBids,
    RawContract,
    RawItems,
    TransformedBidders,
    TransformedBids,
    TransformedContract,
    TransformedItems,
)

############################################################################

CSVContent = str

############################################################################

RawBiddersDF = DataFrame[RawBidders]
RawBidsDF = DataFrame[RawBids]
RawContractDF = DataFrame[RawContract]
RawItemsDF = DataFrame[RawItems]

RawEntitiesDF = RawBiddersDF | RawBidsDF | RawContractDF | RawItemsDF

ExtractFunction = Callable[[CSVContent], RawEntitiesDF]

############################################################################

TransformedBiddersDF = DataFrame[TransformedBidders]
TransformedBidsDF = DataFrame[TransformedBids]
TransformedContractDF = DataFrame[TransformedContract]
TransformedItemsDF = DataFrame[TransformedItems]

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
