from fastapi.testclient import TestClient


def test_api_item_list_etl(test_client: TestClient):
    route_url = "/etl/"

    with open("./tests/data/220005.csv", "rb") as f:
        file = {"csv": f}
        response = test_client.post(url=route_url, files=file)

    assert response.status_code == 200
    response_json = response.json()
    assert response_json["file"] == "220005.csv"
