"""
Sample data from contract 220005
"""
from datetime import datetime

from mndot_bid_api.db import database, models

bidders = [
    models.Bidder(id=0, name="engineer"),
    models.Bidder(id=207897, name="Central Specialties, Inc."),
    models.Bidder(
        id=192907, name="NorthStar Materials, Inc. DBA Knife River Materials"
    ),
    models.Bidder(
        id=857140, name="Anderson Brothers Construction Company of Brainerd, LLC"
    ),
    models.Bidder(id=215861),
    models.Bidder(id=197466),
]

contracts = [
    models.Contract(
        id=220005,
        letting_date=datetime(year=2022, month=1, day=28),
        sp_number="5625-20",
        district="Detroit Lakes",
        county="OTTER TAIL",
        description="LOCATED ON T.H. 108 FROM 420' WEST OF EB T.H. 94 RAMP TO 9TH ST NW.",
        winning_bidder_id=bidders[1].id,
    ),
]

items = [
    models.Item(
        id=1,
        spec_code="2011",
        unit_code="601",
        item_code="01000",
        short_description="AS BUILT",
        long_description="AS BUILT",
        unit="LUMP SUM",
        unit_abbreviation="LS",
        in_spec_2016=True,
        in_spec_2018=True,
        in_spec_2020=True,
        in_spec_2022=False,
    ),
    models.Item(
        id=2,
        spec_code="2106",
        unit_code="507",
        item_code="00010",
        short_description="EXCAVATION - COMMON",
        long_description="EXCAVATION - COMMON",
        unit="CU YD",
        unit_abbreviation="CY",
        in_spec_2016=False,
        in_spec_2018=True,
        in_spec_2020=True,
        in_spec_2022=False,
    ),
]


bids = [
    # AS BUILT bids
    models.Bid(
        id=1,
        contract_id=contracts[0].id,
        bidder_id=bidders[0].id,
        item_id=items[0].id,
        quantity=1,
        unit_price=5_800_00,
        bid_type="engineer",
    ),
    models.Bid(
        id=2,
        contract_id=contracts[0].id,
        bidder_id=bidders[1].id,
        item_id=items[0].id,
        quantity=1,
        unit_price=5_200_00,
        bid_type="winning",
    ),
    models.Bid(
        id=3,
        contract_id=contracts[0].id,
        bidder_id=bidders[2].id,
        item_id=items[0].id,
        quantity=1,
        unit_price=2_700_00,
        bid_type="losing",
    ),
    models.Bid(
        id=4,
        contract_id=contracts[0].id,
        bidder_id=bidders[3].id,
        item_id=items[0].id,
        quantity=1,
        unit_price=10_000_00,
        bid_type="losing",
    ),
    models.Bid(
        id=5,
        contract_id=contracts[0].id,
        bidder_id=bidders[4].id,
        item_id=items[0].id,
        quantity=1,
        unit_price=5_555_00,
        bid_type="losing",
    ),
    models.Bid(
        id=6,
        contract_id=contracts[0].id,
        bidder_id=bidders[5].id,
        item_id=items[0].id,
        quantity=1,
        unit_price=7_500_00,
        bid_type="losing",
    ),
    # EXCAVATION - COMMON bids
    models.Bid(
        id=7,
        contract_id=contracts[0].id,
        bidder_id=bidders[0].id,
        item_id=items[1].id,
        quantity=3725,
        unit_price=15_42,
        bid_type="engineer",
    ),
    models.Bid(
        id=8,
        contract_id=contracts[0].id,
        bidder_id=bidders[1].id,
        item_id=items[1].id,
        quantity=3725,
        unit_price=8_00,
        bid_type="winning",
    ),
    models.Bid(
        id=9,
        contract_id=contracts[0].id,
        bidder_id=bidders[2].id,
        item_id=items[1].id,
        quantity=3725,
        unit_price=4_50,
        bid_type="losing",
    ),
    models.Bid(
        id=10,
        contract_id=contracts[0].id,
        bidder_id=bidders[3].id,
        item_id=items[1].id,
        quantity=3725,
        unit_price=10_88,
        bid_type="losing",
    ),
    models.Bid(
        id=11,
        contract_id=contracts[0].id,
        bidder_id=bidders[4].id,
        item_id=items[1].id,
        quantity=3725,
        unit_price=5_50,
        bid_type="losing",
    ),
    models.Bid(
        id=12,
        contract_id=contracts[0].id,
        bidder_id=bidders[5].id,
        item_id=items[1].id,
        quantity=3725,
        unit_price=6_25,
        bid_type="losing",
    ),
]


invalid_bids = [
    models.InvalidBid(
        id=1,
        contract_id=contracts[0].id,
        bidder_id=bidders[0].id,
        item_spec_code="2564",
        item_unit_code="502",
        item_item_code="00200",
        item_long_description="INSTALL SIGN",
        item_unit_abbreviation="EACH",
        quantity=28,
        unit_price=150_00,
        bid_type="engineer",
    ),
    models.InvalidBid(
        id=2,
        contract_id=contracts[0].id,
        bidder_id=bidders[1].id,
        item_spec_code="2564",
        item_unit_code="502",
        item_item_code="00200",
        item_long_description="INSTALL SIGN",
        item_unit_abbreviation="EACH",
        quantity=28,
        unit_price=315_00,
        bid_type="winning",
    ),
    models.InvalidBid(
        id=3,
        contract_id=contracts[0].id,
        bidder_id=bidders[2].id,
        item_spec_code="2564",
        item_unit_code="502",
        item_item_code="00200",
        item_long_description="INSTALL SIGN",
        item_unit_abbreviation="EACH",
        quantity=28,
        unit_price=315_00,
        bid_type="losing",
    ),
    models.InvalidBid(
        id=4,
        contract_id=contracts[0].id,
        bidder_id=bidders[3].id,
        item_spec_code="2564",
        item_unit_code="502",
        item_item_code="00200",
        item_long_description="INSTALL SIGN",
        item_unit_abbreviation="EACH",
        quantity=28,
        unit_price=552_53,
        bid_type="losing",
    ),
    models.InvalidBid(
        id=5,
        contract_id=contracts[0].id,
        bidder_id=bidders[4].id,
        item_spec_code="2564",
        item_unit_code="502",
        item_item_code="00200",
        item_long_description="INSTALL SIGN",
        item_unit_abbreviation="EACH",
        quantity=28,
        unit_price=350_00,
        bid_type="losing",
    ),
    models.InvalidBid(
        id=6,
        contract_id=contracts[0].id,
        bidder_id=bidders[5].id,
        item_spec_code="2564",
        item_unit_code="502",
        item_item_code="00200",
        item_long_description="INSTALL SIGN",
        item_unit_abbreviation="EACH",
        quantity=28,
        unit_price=315_00,
        bid_type="losing",
    ),
]


def load_sample_data() -> None:
    """Load the database with sample data."""
    with database.DBSession() as db:
        db.add_all(bidders)
        db.add_all(contracts)
        db.add_all(items)
        db.add_all(bids)
        db.add_all(invalid_bids)
        db.commit()
