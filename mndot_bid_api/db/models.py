from sqlalchemy import Boolean, Column, Date, Float, ForeignKey, Index, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


def to_dict(obj: Base):
    """Extract a dictionary of {column_name: value} from a model instance."""
    return {c.name: getattr(obj, c.name) for c in obj.__table__.columns}


class Bidder(Base):
    __tablename__ = "bidder"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=True)


class Contract(Base):
    __tablename__ = "contract"

    id = Column(Integer, primary_key=True)
    letting_date = Column(Date, nullable=False)
    sp_number = Column(String, nullable=False)
    district = Column(String, nullable=False)
    county = Column(String, nullable=False)
    description = Column(String, nullable=False)
    winning_bidder_id = Column(Integer, ForeignKey("bidder.id"), nullable=False)

    # Relationships
    bidder = relationship("Bidder")


class Bid(Base):
    __tablename__ = "bid"

    id = Column(Integer, primary_key=True, autoincrement=True)
    contract_id = Column(Integer, ForeignKey("contract.id"), nullable=False)
    bidder_id = Column(Integer, ForeignKey("bidder.id"), nullable=False)
    item_id = Column(Integer, ForeignKey("item.id"), nullable=False)
    quantity = Column(Float, nullable=False)
    unit_price = Column(Integer, nullable=False)
    bid_type = Column(String, nullable=False)

    # Relationships
    contract = relationship("Contract")
    bidder = relationship("Bidder")
    item = relationship("Item")


Index(
    "ix_invalidbid_definition",
    Bid.contract_id,
    Bid.bidder_id,
    Bid.item_id,
    Bid.quantity,
    Bid.unit_price,
    Bid.bid_type,
)


class InvalidBid(Base):
    __tablename__ = "invalid_bid"

    id = Column(Integer, primary_key=True, autoincrement=True)
    contract_id = Column(Integer, ForeignKey("contract.id"), nullable=False)
    bidder_id = Column(Integer, ForeignKey("bidder.id"), nullable=False)
    item_spec_code = Column(String(4), nullable=False)
    item_unit_code = Column(String(3), nullable=False)
    item_item_code = Column(String(5), nullable=False)
    item_long_description = Column(String, nullable=False)
    item_unit_abbreviation = Column(String, nullable=False)
    quantity = Column(Float, nullable=False)
    unit_price = Column(Integer, nullable=False)
    bid_type = Column(String, nullable=False)

    # Relationships
    contract = relationship("Contract")
    bidder = relationship("Bidder")


Index(
    "ix_bid_definition",
    InvalidBid.contract_id,
    InvalidBid.bidder_id,
    InvalidBid.item_spec_code,
    InvalidBid.item_unit_code,
    InvalidBid.item_item_code,
    InvalidBid.item_long_description,
    InvalidBid.item_unit_abbreviation,
    InvalidBid.quantity,
    InvalidBid.unit_price,
    InvalidBid.bid_type,
)


class Item(Base):
    __tablename__ = "item"

    id = Column(Integer, primary_key=True, autoincrement=True)
    spec_code = Column(String(4), nullable=False)
    unit_code = Column(String(3), nullable=False)
    item_code = Column(String(5), nullable=False)
    short_description = Column(String, nullable=False)
    long_description = Column(String, nullable=False)
    unit = Column(String, nullable=False)
    unit_abbreviation = Column(String, nullable=False)
    in_spec_2016 = Column(Boolean, nullable=False, default=False)
    in_spec_2018 = Column(Boolean, nullable=False, default=False)
    in_spec_2020 = Column(Boolean, nullable=False, default=False)
    in_spec_2022 = Column(Boolean, nullable=False, default=False)


Index(
    "ix_item_definition",
    Item.spec_code,
    Item.unit_code,
    Item.item_code,
    Item.short_description,
    Item.long_description,
    Item.unit,
    Item.unit_abbreviation,
)

Index(
    "ix_create_bid_search",
    Item.spec_code,
    Item.unit_code,
    Item.item_code,
    Item.long_description,
    Item.unit_abbreviation,
)


class AbstractETLStatus(Base):
    __tablename__ = "etlstatus"

    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime, nullable=False)
    contract_id = Column(Integer, nullable=False)
    csv_downloaded = Column(Boolean, nullable=True)
    extracted = Column(Boolean, nullable=True)
    transformed = Column(Boolean, nullable=True)
    loaded = Column(Boolean, nullable=True)
    successful = Column(Boolean, nullable=True)
    error_msg = Column(String, nullable=True)