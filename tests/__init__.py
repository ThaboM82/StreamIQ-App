import pytest
from src.app import app

@pytest.fixture
def client():
    app.testing = True
    return app.test_client()

def test_api_predict(client):
    response = client.post("/predict", json={"text": "Great service"})
    assert response.status_code == 200
    data = response.get_json()
    assert "score" in data
    assert isinstance(data["score"], float)
