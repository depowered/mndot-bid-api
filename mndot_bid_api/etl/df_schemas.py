import pandera as pa


class RawItems(pa.SchemaModel):
    ...


class TransformedItems(pa.SchemaModel):
    ...


class RawContract(pa.SchemaModel):
    ...


class TransformedContract(pa.SchemaModel):
    ...


class RawBidders(pa.SchemaModel):
    ...


class TransformedBidders(pa.SchemaModel):
    ...


class RawBids(pa.SchemaModel):
    ...


class TransformedBids(pa.SchemaModel):
    ...
