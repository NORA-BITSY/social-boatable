from backend.social.app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)

def _login():
    client.post("/users/", json={"username": "g1", "email": "g1@x.z", "password": "p", "roles":["VENDOR"]})
    tok = client.post(
        "/auth/token",
        data={"username": "g1", "password": "p"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    ).json()["access_token"]
    return {"Authorization": f"Bearer {tok}"}

def test_group_lifecycle():
    hdr = _login()
    create = client.post("/groups/", json={"name": "Sail Club"}, headers=hdr)
    assert create.status_code == 201
    assert create.json()["name"] == "Sail Club"

    all_groups = client.get("/groups/", headers=hdr).json()
    assert any(g["name"] == "Sail Club" for g in all_groups)

    single = client.get("/groups/Sail Club", headers=hdr)
    assert single.status_code == 200
