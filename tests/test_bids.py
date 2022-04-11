from random import randint
from fastapi.testclient import TestClient
from fastapi.encoders import jsonable_encoder

from main import app, startup_event
from mndot_bid_api.db.models import to_dict
from mndot_bid_api.db.sample_data import bids
from mndot_bid_api.operations.models import BidCreateData, BidUpdateData


startup_event()
client = TestClient(app)


def test_api_read_all_bids():
    response = client.get("/bids")
    assert response.status_code == 200

    data = response.json()
    data_list = list(data)
    assert len(data_list) > 0
    assert data_list[0] == jsonable_encoder(bids[0])


def test_api_read_bid():
    response = client.get("/bid/1")
    assert response.status_code == 200
    data = response.json()
    assert data == jsonable_encoder(bids[0])


def test_api_read_bid_not_in_db():
    bid_id = -2
    response = client.get(f"/bid/{bid_id}")
    assert response.status_code == 404


def test_api_create_bid():
    payload = BidCreateData(
        item_number="2501.503/12345",
        spec_year=2020,
        quantity=300.0,
        unit_price=6_00,
        total_price=int(300.0 * 6_00),
        contract_id=randint(100, 3_000_000),
        bidder_id=3,
        bidder_rank=1,
    ).dict()

    response = client.post("/bid", json=payload)
    assert response.status_code == 200


def test_api_create_bid_does_not_duplicate():
    payload = BidCreateData(**to_dict(bids[0])).dict()
    response = client.post("/bid", json=payload)
    assert response.status_code == 303


def test_api_update_bid():
    new_quantity = randint(1, 500)
    bid_update = BidUpdateData(quantity=new_quantity)
    payload = bid_update.dict()
    response = client.put("/bid/3", json=payload)
    assert response.status_code == 200

    data = response.json()
    assert data["quantity"] == new_quantity
