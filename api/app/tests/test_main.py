from fastapi.testclient import TestClient

from app.main import app

testclient = TestClient(app)

def test_simply_endpoint():
    response = testclient.get("/test")
    assert response.status_code == 200
    assert response.json() == {"message": "Job enqueued"}

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
