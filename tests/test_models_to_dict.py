from mndot_bid_api.db import models


def test_to_dict_with_bidder_model():
    data = {"id": 207897, "name": "Central Specialties, Inc."}
    result = models.to_dict(models.Bidder(**data))

    assert data == result


def test_to_dict_with_contract_model():
    data = {
        "id": 220005,
        "letting_date": "2022-01-28",
        "sp_number": "5625-20",
        "district": "Detroit Lakes",
        "county": "OTTER TAIL",
        "description": "LOCATED ON T.H. 108 FROM 420' WEST OF EB T.H. 94 RAMP TO 9TH ST NW.",
        "winning_bidder_id": 207897,
    }
    result = models.to_dict(models.Contract(**data))

    assert data == result


def test_to_dict_with_bid_model():
    data = {
        "id": 1,
        "contract_id": 220005,
        "bidder_id": 207897,
        "item_id": 1,
        "quantity": 1,
        "unit_price": 5_200_00,
        "bid_type": "winning",
    }
    result = models.to_dict(models.Bid(**data))

    assert data == result


def test_to_dict_with_invalid_bid_model():
    data = {
        "id": 2,
        "contract_id": 220005,
        "bidder_id": 207897,
        "item_spec_code": "2564",
        "item_unit_code": "502",
        "item_item_code": "00200",
        "item_long_description": "INSTALL SIGN",
        "item_unit_abbreviation": "EACH",
        "quantity": 28,
        "unit_price": 315_00,
        "bid_type": "winning",
    }
    result = models.to_dict(models.InvalidBid(**data))

    assert data == result


def test_to_dict_with_item_model():
    data = {
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
    }
    result = models.to_dict(models.Item(**data))

    assert data == result


def test_bidder_name_is_nullable():
    data = {"id": 100}
    expected = {"id": 100, "name": None}
    result = models.to_dict(models.Bidder(**data))

    assert result == expected
