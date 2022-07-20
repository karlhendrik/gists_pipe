from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200

def test_get_gists_from_github():
    response = client.get("/api/v1/gists")
    assert response.status_code == 200
    assert len(response.json()) == 30

def test_get_deals_from_pipedrive():
    response = client.get("/api/v1/deals")
    assert response.status_code == 200