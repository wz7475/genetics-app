import requests
import pytest

URL = "http://api:80"
URL = "http://localhost:8080"


def post_file():
    url = f"{URL}/uploadFile"
    files = {"file": open("taskflowapi/data/2rec.tsv", "rb")}
    data = {"algorithms": "pangolin,spip"}
    return requests.post(url, files=files, data=data)


@pytest.mark.run(order=1)
def test_basic_endpoint():
    response = requests.get(f"{URL}/availableAlgorithms")
    assert response.json() == {"algorithms": ["pangolin", "spip"]}
    assert response.status_code == 200


@pytest.mark.run(order=2)
def test_upload_file():
    response = post_file()
    assert response.status_code == 200
    response = response.json()
    assert response["message"] == "success"
    assert type(response["id"]) is str


@pytest.mark.run(order=3)
def test_get_status_expired():
    url = f"{URL}/getStatus"
    data = {"task_id": "random_id"}
    response = requests.post(url, data=data)
    assert response.status_code == 200
    assert response.json() == {"status": "expired"}


@pytest.mark.run(order=4)
def test_get_status_pending():
    response = post_file()
    task_id = response.json()["id"]
    response = requests.post(f"{URL}/getStatus", data=f'"{task_id}"')
    assert response.status_code == 200
    assert response.json()["status"] == "pending"


@pytest.mark.run(order=5)
def test_get_detailed_status():
    response = post_file()
    task_id = response.json()["id"]
    response = requests.post(f"{URL}/getDetailedStatus", data=f'"{task_id}"')
    assert response.status_code == 200
    response = response.json()["status"]
    assert "pangolin" in response
    assert "spip" in response
    assert "status" in response
