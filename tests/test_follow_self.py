from backend.social.app.main import app
from fastapi.testclient import TestClient
from fastapi import status

client = TestClient(app)

def _login(username="u", email="u@x.z"):
    client.post("/users/", json={"username": username, "email": email, "password": "p"})
    tok = client.post(
        "/auth/token",
        data={"username": username, "password": "p"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    ).json()["access_token"]
    return {"Authorization": f"Bearer {tok}"}

def test_follow_self():
    alice = _login("alice", "a@x.z")
    response = client.post("/users/alice/follow", headers=alice)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
