from backend.social.app.main import app as social_app
from backend.marketplace.app.main import app as marketplace_app
from fastapi.testclient import TestClient

# boot social first (ensures tables)
social_client = TestClient(social_app)
mp_client     = TestClient(marketplace_app)


def test_create_service_and_order():
    # 1️⃣ Register & login through the in-process social API
    user_resp = social_client.post(
        "/users/",
        json={"username": "bob", "email": "bob@test.io", "password": "pass123"},
    )
    assert user_resp.status_code == 201

    token_resp = social_client.post(
        "/auth/token",
        data={"username": "bob", "password": "pass123"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert token_resp.status_code == 200
    token = token_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 2️⃣ Provider creates a service listing
    svc_resp = mp_client.post(
        "/services/",
        json={
            "title": "Hull Cleaning",
            "description": "Basic wash",
            "category": "cleaning",
            "price": 100,
        },
        headers=headers,
    )
    assert svc_resp.status_code == 201
    svc_id = svc_resp.json()["id"]

    # 3️⃣ Same user books that service
    order_resp = mp_client.post(
        "/orders/",
        json={"service_id": svc_id, "quantity": 2},
        headers=headers,
    )
    assert order_resp.status_code == 201
    assert order_resp.json()["total"] == 200
