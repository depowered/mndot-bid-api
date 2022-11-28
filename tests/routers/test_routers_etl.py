import pytest
from fastapi.testclient import TestClient


@pytest.mark.skipif(
    "not config.getoption('--run-slow')",
    reason="Only run when --run-slow is given",
)
def test_api_item_list_etl(test_client: TestClient):
    route_url = "/etl/"

    with open("./tests/data/item_list_2018.csv", "rb") as f:
        file = {"csv": f}
        response = test_client.post(url=route_url, files=file)

    assert response.status_code == 200
    response_json = response.json()
    assert response_json["spec_year"] == "2018"
    assert len(response_json["item_results"]) == 8032
