from fastapi.testclient import TestClient


def test_api_item_list_etl(test_client: TestClient, abstract_csv_file):
    route_url = "/etl/"

    file = {"csv": abstract_csv_file}
    response = test_client.post(url=route_url, files=file)

    assert response.status_code == 200
    response_json = response.json()
    assert response_json["file"] == "220005.csv"
