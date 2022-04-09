from fastapi.testclient import TestClient
from fastapi.encoders import jsonable_encoder

from main import app, startup_event
from mndot_bid_api.db.models import DBBidder
from mndot_bid_api.db.sample_data import bidders

startup_event()
client = TestClient(app)


def test_api_read_all_bidders():
    response = client.get("/bidders")
    assert response.status_code == 200

    data = response.json()
    data_list = list(response.json())
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
    assert response.status_code == 200
    data = response.json()
    assert data == {"message": f"Bidder with ID {bidder_id} not found."}
