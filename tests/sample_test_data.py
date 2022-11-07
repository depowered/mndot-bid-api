sample_bidders = [
    {"id": 0, "name": "engineer"},
    {"id": 207897, "name": "Central Specialties, Inc."},
    {"id": 192907, "name": "NorthStar Materials, Inc. DBA Knife River Materials"},
    {"id": 857140, "name": "Anderson Brothers Construction Company of Brainerd, LLC"},
    {"id": 215861, "name": None},
    {"id": 197466, "name": None},
]

sample_contracts = [
    {
        "id": 220005,
        "letting_date": "2022-01-28",
        "sp_number": "5625-20",
        "district": "Detroit Lakes",
        "county": "OTTER TAIL",
        "description": "LOCATED ON T.H. 108 FROM 420' WEST OF EB T.H. 94 RAMP TO 9TH ST NW.",
        "winning_bidder_id": 207897,
    },
]

sample_items = [
    {
        "id": 1,
        "spec_code": "2011",
        "unit_code": "601",
        "item_code": "01000",
        "short_description": "AS BUILT",
        "long_description": "AS BUILT",
        "unit": "LUMP SUM",
        "unit_abbreviation": "LS",
        "in_spec_2016": True,
        "in_spec_2018": True,
        "in_spec_2020": True,
        "in_spec_2022": False,
    },
    {
        "id": 2,
        "spec_code": "2106",
        "unit_code": "507",
        "item_code": "00010",
        "short_description": "EXCAVATION - COMMON",
        "long_description": "EXCAVATION - COMMON",
        "unit": "CU YD",
        "unit_abbreviation": "CY",
        "in_spec_2016": False,
        "in_spec_2018": True,
        "in_spec_2020": True,
        "in_spec_2022": False,
    },
]

sample_bids = [
    {
        "id": 1,
        "contract_id": 220005,
        "bidder_id": 0,
        "item_id": 1,
        "quantity": 1,
        "unit_price": 580000,
        "bid_type": "engineer",
    },
    {
        "id": 2,
        "contract_id": 220005,
        "bidder_id": 207897,
        "item_id": 1,
        "quantity": 1,
        "unit_price": 520000,
        "bid_type": "winning",
    },
    {
        "id": 3,
        "contract_id": 220005,
        "bidder_id": 192907,
        "item_id": 1,
        "quantity": 1,
        "unit_price": 270000,
        "bid_type": "losing",
    },
    {
        "id": 4,
        "contract_id": 220005,
        "bidder_id": 857140,
        "item_id": 1,
        "quantity": 1,
        "unit_price": 1000000,
        "bid_type": "losing",
    },
    {
        "id": 5,
        "contract_id": 220005,
        "bidder_id": 215861,
        "item_id": 1,
        "quantity": 1,
        "unit_price": 555500,
        "bid_type": "losing",
    },
    {
        "id": 6,
        "contract_id": 220005,
        "bidder_id": 197466,
        "item_id": 1,
        "quantity": 1,
        "unit_price": 750000,
        "bid_type": "losing",
    },
    {
        "id": 7,
        "contract_id": 220005,
        "bidder_id": 0,
        "item_id": 2,
        "quantity": 3725,
        "unit_price": 1542,
        "bid_type": "engineer",
    },
    {
        "id": 8,
        "contract_id": 220005,
        "bidder_id": 207897,
        "item_id": 2,
        "quantity": 3725,
        "unit_price": 800,
        "bid_type": "winning",
    },
    {
        "id": 9,
        "contract_id": 220005,
        "bidder_id": 192907,
        "item_id": 2,
        "quantity": 3725,
        "unit_price": 450,
        "bid_type": "losing",
    },
    {
        "id": 10,
        "contract_id": 220005,
        "bidder_id": 857140,
        "item_id": 2,
        "quantity": 3725,
        "unit_price": 1088,
        "bid_type": "losing",
    },
    {
        "id": 11,
        "contract_id": 220005,
        "bidder_id": 215861,
        "item_id": 2,
        "quantity": 3725,
        "unit_price": 550,
        "bid_type": "losing",
    },
    {
        "id": 12,
        "contract_id": 220005,
        "bidder_id": 197466,
        "item_id": 2,
        "quantity": 3725,
        "unit_price": 625,
        "bid_type": "losing",
    },
]

sample_invalid_bids = [
    {
        "id": 1,
        "contract_id": 220005,
        "bidder_id": 0,
        "item_spec_code": "2564",
        "item_unit_code": "502",
        "item_item_code": "00200",
        "item_long_description": "INSTALL SIGN",
        "item_unit_abbreviation": "EACH",
        "quantity": 28,
        "unit_price": 15000,
        "bid_type": "engineer",
    },
    {
        "id": 2,
        "contract_id": 220005,
        "bidder_id": 207897,
        "item_spec_code": "2564",
        "item_unit_code": "502",
        "item_item_code": "00200",
        "item_long_description": "INSTALL SIGN",
        "item_unit_abbreviation": "EACH",
        "quantity": 28,
        "unit_price": 31500,
        "bid_type": "winning",
    },
    {
        "id": 3,
        "contract_id": 220005,
        "bidder_id": 192907,
        "item_spec_code": "2564",
        "item_unit_code": "502",
        "item_item_code": "00200",
        "item_long_description": "INSTALL SIGN",
        "item_unit_abbreviation": "EACH",
        "quantity": 28,
        "unit_price": 31500,
        "bid_type": "losing",
    },
    {
        "id": 4,
        "contract_id": 220005,
        "bidder_id": 857140,
        "item_spec_code": "2564",
        "item_unit_code": "502",
        "item_item_code": "00200",
        "item_long_description": "INSTALL SIGN",
        "item_unit_abbreviation": "EACH",
        "quantity": 28,
        "unit_price": 55253,
        "bid_type": "losing",
    },
    {
        "id": 5,
        "contract_id": 220005,
        "bidder_id": 215861,
        "item_spec_code": "2564",
        "item_unit_code": "502",
        "item_item_code": "00200",
        "item_long_description": "INSTALL SIGN",
        "item_unit_abbreviation": "EACH",
        "quantity": 28,
        "unit_price": 35000,
        "bid_type": "losing",
    },
    {
        "id": 6,
        "contract_id": 220005,
        "bidder_id": 197466,
        "item_spec_code": "2564",
        "item_unit_code": "502",
        "item_item_code": "00200",
        "item_long_description": "INSTALL SIGN",
        "item_unit_abbreviation": "EACH",
        "quantity": 28,
        "unit_price": 31500,
        "bid_type": "losing",
    },
]
