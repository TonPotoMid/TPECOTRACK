from fastapi.testclient import TestClient
from app.main import app
import uuid


client = TestClient(app)


def test_register_and_login():
    # use a random email to avoid conflicts
    email = f"test+{uuid.uuid4().hex[:8]}@example.com"
    password = "testpass123"

    # register
    r = client.post("/auth/register", json={"email": email, "password": password})
    assert r.status_code == 200, r.text
    data = r.json()
    assert data["email"] == email

    # login (OAuth2PasswordRequestForm expects form data)
    r = client.post("/auth/login", data={"username": email, "password": password})
    assert r.status_code == 200, r.text
    token = r.json().get("access_token")
    assert token and isinstance(token, str)
