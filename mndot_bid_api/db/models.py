from sqlalchemy import Column, Computed, Date, Float, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


def to_dict(obj: Base):
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
    spec_year = Column(String, nullable=False)

    # Relationships
    bidder = relationship("Bidder")


class Bid(Base):
    __tablename__ = "bid"

    id = Column(Integer, primary_key=True, autoincrement=True)
    contract_id = Column(Integer, ForeignKey("contract.id"), nullable=False)
    item_composite_id = Column(String, ForeignKey("item.composite_id"), nullable=False)
    bidder_id = Column(Integer, ForeignKey("bidder.id"), nullable=False)
    quantity = Column(Float, nullable=False)
    unit_price = Column(Integer, nullable=False)
    bid_type = Column(
        String, nullable=False
    )  # "engineers_estimate", "winning_bid", or "losing_bid"

    # Relationships
    contract = relationship("Contract")
    bidder = relationship("Bidder")
    item = relationship("Item")


class Item(Base):
    __tablename__ = "item"

    id = Column(Integer, primary_key=True, autoincrement=True)
    composite_id = Column(String, nullable=False)
    spec_year = Column(String(4), nullable=False)
    spec_code = Column(String(4), nullable=False)
    unit_code = Column(String(3), nullable=False)
    item_code = Column(String(5), nullable=False)
    short_description = Column(String, nullable=False)
    long_description = Column(String, nullable=False)
    unit = Column(String, nullable=False)
    unit_abreviation = Column(String, nullable=False)
