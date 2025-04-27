from backend.social.app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)

def _login(username="u", email="u@x.z"):
    client.post("/users/", json={"username": username, "email": email, "password": "p"})
    tok = client.post(
        "/auth/token",
        data={"username": username, "password": "p"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    ).json()["access_token"]
    return {"Authorization": f"Bearer {tok}"}

def test_message_triggers_notification():
    alice = _login("alice", "a@x.z")
    bob   = _login("bob", "b@x.z")
    # send DM
    client.post("/messages/", params={"receiver_id": 2},
                json={"content":"hi"}, headers=alice)
    notes = client.get("/notifications/", headers=bob).json()
    assert any(n["type"] == "message" for n in notes)
