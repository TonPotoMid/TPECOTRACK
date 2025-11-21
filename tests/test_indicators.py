from fastapi.testclient import TestClient
from app.main import app
from app import database
import pytest


client = TestClient(app)


def get_admin_token():
    # uses seed credentials created by scripts/seed_db.py
    r = client.post("/auth/login", data={"username": "admin@example.com", "password": "adminpass"})
    if r.status_code != 200:
        pytest.skip("Admin credentials not available (run scripts/seed_db.py)")
    return r.json()["access_token"]


def test_create_and_list_indicator():
    token = get_admin_token()
    headers = {"Authorization": f"Bearer {token}"}

    # create an indicator
    payload = {
        "source_id": None,
        "type": "pm25",
        "value": 10.5,
        "unit": "µg/m3",
        "zone_id": None,
    }
    r = client.post("/indicators/", json=payload, headers=headers)
    assert r.status_code == 200, r.text
    created = r.json()
    assert created["type"] == "pm25"

    # list indicators
    r = client.get("/indicators/", headers=headers)
    assert r.status_code == 200, r.text
    arr = r.json()
    assert isinstance(arr, list)
    assert any(item["id"] == created["id"] for item in arr)
