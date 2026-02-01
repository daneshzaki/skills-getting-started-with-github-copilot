import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "participants" in data["Chess Club"]

def test_signup_for_activity():
    # Test successful signup
    response = client.post("/activities/Chess Club/signup?email=test@example.com")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data

    # Test duplicate signup
    response = client.post("/activities/Chess Club/signup?email=test@example.com")
    assert response.status_code == 400

def test_signup_nonexistent_activity():
    response = client.post("/activities/Nonexistent Activity/signup?email=test@example.com")
    assert response.status_code == 404

def test_unregister_from_activity():
    # First signup
    client.post("/activities/Chess Club/signup?email=unregister@example.com")

    # Then unregister
    response = client.delete("/activities/Chess Club/unregister?email=unregister@example.com")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data

    # Test unregistering someone not signed up
    response = client.delete("/activities/Chess Club/unregister?email=notsignedup@example.com")
    assert response.status_code == 400

def test_unregister_nonexistent_activity():
    response = client.delete("/activities/Nonexistent Activity/unregister?email=test@example.com")
    assert response.status_code == 404