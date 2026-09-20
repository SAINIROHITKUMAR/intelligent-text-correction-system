from app import create_app

def test_health():
    client = create_app().test_client()
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.get_json()["status"] == "ok"

def test_correct_endpoint():
    client = create_app().test_client()
    response = client.post("/api/correct", json={"text": "I definately recieve teh email."})
    assert response.status_code == 200
    data = response.get_json()
    assert data["corrected_text"] == "I definitely receive the email."
    assert data["change_count"] == 3

def test_empty_input():
    client = create_app().test_client()
    response = client.post("/api/correct", json={"text": "   "})
    assert response.status_code == 400
