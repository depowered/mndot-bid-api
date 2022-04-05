from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


def to_dict(obj: Base):
    return {c.name: getattr(obj, c.name) for c in obj.__table__.columns}


class DBBidder(Base):
    __tablename__ = "bidder"

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=True)


class DBContract(Base):
    __tablename__ = "contract"

    id = Column(Integer, primary_key=True)
    is_processed = Column(Boolean, nullable=False)
    let_date = Column(Date, nullable=True)
    let_year = Column(Integer, nullable=True)
    spec_year = Column(Integer, nullable=True)
    sp_number = Column(String(30), nullable=True)
    district = Column(String(30), nullable=True)
    county = Column(String(30), nullable=True)
    engineers_total = Column(Integer, nullable=True)

    lowest_bidder_id = Column(Integer, ForeignKey("bidder.id"), nullable=True)
    bidder = relationship(DBBidder)
    lowest_bidder_total = Column(Integer, nullable=True)


class DBBid(Base):
    __tablename__ = "bid"

    id = Column(Integer, primary_key=True, autoincrement=True)
    item_number = Column(String(14), nullable=False)
    spec_year = Column(Integer, nullable=False)
    quantity = Column(Float, nullable=False)
    unit_price = Column(Integer, nullable=False)
    total_price = Column(Integer, nullable=False)

    contract_id = Column(Integer, ForeignKey("contract.id"), nullable=False)
    contract = relationship(DBContract)
    bidder_id = Column(Integer, ForeignKey("bidder.id"), nullable=False)
    bidder = relationship(DBBidder)
    bidder_rank = Column(Integer, nullable=False)


class DBItems2018(Base):
    __tablename__ = "items2018"

    id = Column(Integer, primary_key=True, autoincrement=True)
    item_number = Column(String(14), nullable=False)
    description = Column(String(250), nullable=False)
    units = Column(String(30), nullable=True)


class DBItems2020(Base):
    __tablename__ = "items2020"

    id = Column(Integer, primary_key=True, autoincrement=True)
    item_number = Column(String(14), nullable=False)
    description = Column(String(250), nullable=False)
    units = Column(String(30), nullable=True)
