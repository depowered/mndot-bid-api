from fastapi.testclient import TestClient

from tests.data import sample_record_dicts


def test_api_query_bidder(test_client: TestClient):
    route_url = "/bidder/query/"

    # Test with valid kwarg & value
    path_params = "?name=engineer"
    response = test_client.get(route_url + path_params)
    assert response.status_code == 200

    response_json = response.json()
    assert response_json["type"] == "BidderCollection"
    record_dict = response_json["data"][0]
    assert record_dict == sample_record_dicts.sample_bidders[0]

    # Test with valid kwarg & invalid value
    path_params = "?name=nobody"
    response = test_client.get(route_url + path_params)
    assert response.status_code == 404

    # Test with invalid kwarg & value
    path_params = "?NotAKey=nobody"
    response = test_client.get(route_url + path_params)
    assert response.status_code == 400


def test_api_query_contract(test_client: TestClient):
    route_url = "/contract/query/"

    # Test with valid kwarg & value
    path_params = "?letting_date=2022-01-28"
    expected_record_dict = {
        "id": 220005,
        "letting_date": "2022-01-28",
        "sp_number": "5625-20",
        "district": "Detroit Lakes",
        "county": "OTTER TAIL",
        "description": "LOCATED ON T.H. 108 FROM 420' WEST OF EB T.H. 94 RAMP TO 9TH ST NW.",
        "winning_bidder_id": 207897,
    }

    response = test_client.get(route_url + path_params)
    assert response.status_code == 200

    response_json = response.json()
    assert response_json["type"] == "ContractCollection"
    record_dict = response_json["data"][0]
    assert record_dict == expected_record_dict

    # Test with valid kwarg & invalid value
    path_params = "?district=NotHere"
    response = test_client.get(route_url + path_params)
    assert response.status_code == 404

    # Test with invalid kwarg & value
    path_params = "?NotAKey=nobody"
    response = test_client.get(route_url + path_params)
    assert response.status_code == 400


def test_api_query_item(test_client: TestClient):
    route_url = "/item/query/"

    # Test with valid kwarg & value
    path_params = "?spec_code=2011&unit_code=601&item_code=01000"
    expected_record_dict = sample_record_dicts.sample_items[0]

    response = test_client.get(route_url + path_params)
    assert response.status_code == 200

    response_json = response.json()
    assert response_json["type"] == "ItemCollection"
    record_dict = response_json["data"][0]
    assert record_dict == expected_record_dict

    # Test with valid kwarg & invalid value
    path_params = "?spec_code=9999"
    response = test_client.get(route_url + path_params)
    assert response.status_code == 404

    # Test with invalid kwarg & value
    path_params = "?NotAKey=nobody"
    response = test_client.get(route_url + path_params)
    assert response.status_code == 400


def test_api_query_bid(test_client: TestClient):
    route_url = "/bid/query/"

    # Test with valid kwarg & value
    path_params = "?contract_id=220005&bidder_id=207897&item_id=1"
    expected_record_dict = sample_record_dicts.sample_bids[1]

    response = test_client.get(route_url + path_params)
    assert response.status_code == 200

    response_json = response.json()
    assert response_json["type"] == "BidCollection"
    record_dict = response_json["data"][0]
    assert record_dict == expected_record_dict

    # Test with valid kwarg & invalid value
    path_params = "?contract_id=-7"
    response = test_client.get(route_url + path_params)
    assert response.status_code == 404

    # Test with invalid kwarg & value
    path_params = "?NotAKey=nobody"
    response = test_client.get(route_url + path_params)
    assert response.status_code == 400


def test_api_query_invalid_bid(test_client: TestClient):
    route_url = "/invalid_bid/query/"

    # Test with valid kwarg & value
    path_params = "?contract_id=220005&bidder_id=207897&quantity=28"
    expected_record_dict = sample_record_dicts.sample_invalid_bids[1]

    response = test_client.get(route_url + path_params)
    assert response.status_code == 200

    response_json = response.json()
    assert response_json["type"] == "InvalidBidCollection"
    record_dict = response_json["data"][0]
    assert record_dict == expected_record_dict

    # Test with valid kwarg & invalid value
    path_params = "?contract_id=-7"
    response = test_client.get(route_url + path_params)
    assert response.status_code == 404

    # Test with invalid kwarg & value
    path_params = "?NotAKey=nobody"
    response = test_client.get(route_url + path_params)
    assert response.status_code == 400
