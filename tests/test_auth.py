from backend.social.app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_login_and_protected_endpoint():
    # create a user first
    user_resp = client.post(
        "/users/",
        json={"username": "alice", "email": "alice@test.io", "password": "pass123"},
    )
    assert user_resp.status_code == 201

    # login
    token_resp = client.post(
        "/auth/token",
        data={"username": "alice", "password": "pass123"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert token_resp.status_code == 200
    token = token_resp.json()["access_token"]

    # call protected list users
    protected = client.get("/users/", headers={"Authorization": f"Bearer {token}"})
    assert protected.status_code == 200
    assert any(u["username"] == "alice" for u in protected.json())
