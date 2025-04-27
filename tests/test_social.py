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

def test_follow_and_feed():
    alice_hdr = _login("alice", "alice@x.z")
    bob_hdr   = _login("bob", "bob@x.z")

    # Alice follows Bob
    client.post("/users/bob/follow", headers=alice_hdr)

    # Bob creates a post
    client.post("/posts/", headers=bob_hdr, json={"content": "Ahoy!", "privacy": "public", "type": "status"})

    # Alice sees Bob's post in her feed
    feed = client.get("/feed/", headers=alice_hdr).json()
    assert any(p["content"] == "Ahoy!" for p in feed)
