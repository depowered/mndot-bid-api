from random import randint
from fastapi.testclient import TestClient
from fastapi.encoders import jsonable_encoder

from main import app, startup_event
from mndot_bid_api.db.models import to_dict
from mndot_bid_api.db.sample_data import bidders
from mndot_bid_api.operations.schema import BidderCreateData, BidderUpdateData

startup_event()
client = TestClient(app)


def test_api_read_all_bidders():
    response = client.get("/bidders")
    assert response.status_code == 200

    data = response.json()
    data_list = list(data)
    assert len(data_list) > 0
    assert data_list[0] == jsonable_encoder(bidders[0])


def test_api_read_bidder():
    response = client.get("/bidder/1")
    assert response.status_code == 200
    data = response.json()
    assert data == jsonable_encoder(bidders[0])


def test_api_read_bidder_not_in_db():
    bidder_id = -1
    response = client.get(f"/bidder/{bidder_id}")
    assert response.status_code == 404


def test_api_create_bidder():
    bidder = BidderCreateData(id=randint(100, 3_000_000), name="Contractor No. 300")

    payload = bidder.dict()
    response = client.post("/bidder", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data == jsonable_encoder(bidder)


def test_api_create_bidder_does_not_duplicate():
    bidder = BidderCreateData(**to_dict(bidders[0]))
    payload = bidder.dict()
    response = client.post("/bidder", json=payload)
    assert response.status_code == 303


def test_api_update_bidder():
    new_name = f"Contractor No. {str(randint(1_000, 100_000))}"
    bidder_update = BidderUpdateData(name=new_name)
    payload = bidder_update.dict()
    response = client.patch("/bidder/2", json=payload)
    assert response.status_code == 200

    data = response.json()
    assert data["name"] == new_name
