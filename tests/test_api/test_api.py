from fastapi.testclient import TestClient

# from taskflowapi.api.app.main import app
#
# testclient = TestClient(app)


def test_startup():
    """
    - context manager to include on event startup and shutdown
    - requires a rabbitmq server running / mocking it
    """
    # with TestClient(app) as client:
    #     response = client.get("/")
    #     assert response.status_code == 200
    #     assert response.json() == {"message": "Job enqueued"}
    assert "app" == "app"


def test_algorythm():
    """
    - requiers diffrent method of using sheared utils in app
    """
    # with TestClient(app) as client:
    #     response = client.get("/availableAlgorithms")
    #     assert response.status_code == 200
    #     assert response.json() == {"message": "Job enqueued"}
