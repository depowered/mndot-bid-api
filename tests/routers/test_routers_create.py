import json

from fastapi.testclient import TestClient


def test_api_create_bid(test_client: TestClient):
    route_url = "/bid/"

    # Test valid bid create data
    create_data = {
        "contract_id": 1,
        "bidder_id": 0,
        "item_spec_code": "2011",
        "item_unit_code": "601",
        "item_item_code": "01000",
        "item_long_description": "AS BUILT",
        "item_unit_abbreviation": "LS",
        "quantity": 1,
        "unit_price": 5_000_00,
        "bid_type": "engineer",
    }

    response = test_client.post(url=route_url, data=json.dumps(create_data))
    assert response.status_code == 201

    response_json = response.json()
    assert response_json["type"] == "Bid"
    record_dict = response_json["data"]
    assert record_dict.get("id")

    # Test invalid bid create data
    invalid_create_data = {
        "contract_id": 1,
        "bidder_id": 0,
        "item_spec_code": "1111",
        "item_unit_code": "222",
        "item_item_code": "33333",
        "item_long_description": "AS BUILT",
        "item_unit_abbreviation": "LS",
        "quantity": 1,
        "unit_price": 5_000_00,
        "bid_type": "engineer",
    }

    response = test_client.post(url=route_url, data=json.dumps(invalid_create_data))
    assert response.status_code == 307


def test_api_create_item(test_client: TestClient):
    route_url = "/item/"

    # # Test valid item create data
    create_data = {
        "spec_code": "2021",
        "unit_code": "501",
        "item_code": "01000",
        "short_description": "MOBILIZATION",
        "long_description": "MOBILIZATION",
        "unit": "LUMP SUM",
        "unit_abbreviation": "LS",
        "in_spec_2016": True,
        "in_spec_2018": True,
        "in_spec_2020": True,
        "in_spec_2022": False,
    }

    response = test_client.post(url=route_url, data=json.dumps(create_data))
    assert response.status_code == 201

    response_json = response.json()
    assert response_json["type"] == "Item"
    record_dict = response_json["data"]
    assert record_dict.get("in_spec_2022") is False

    # Test posting existing record raises status 303
    existing_record = {
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
        "in_spec_2022": True,  # Changed to True
    }

    response = test_client.post(url=route_url, data=json.dumps(existing_record))
    assert response.status_code == 303
