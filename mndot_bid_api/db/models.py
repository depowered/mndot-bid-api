from sqlalchemy import Boolean, Column, Date, Float, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


def to_dict(obj: Base):
    return {c.name: getattr(obj, c.name) for c in obj.__table__.columns}


def get_columns_list(obj: Base):
    return [c.name for c in obj.__table__.columns]


class Bidder(Base):
    __tablename__ = "bidder"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)


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
    in_spec_2016 = Column(Boolean, nullable=False)
    in_spec_2018 = Column(Boolean, nullable=False)
    in_spec_2020 = Column(Boolean, nullable=False)
    in_spec_2022 = Column(Boolean, nullable=False)
