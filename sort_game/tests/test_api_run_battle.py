def test_run_battle_success(client):
    payload = {
        "array_size": 2000
    }

    response = client.post("/api/run-battle", json=payload)
    assert response.status_code == 200

    body = response.get_json()
    assert body is not None
    assert body["success"] is True
    assert body["error"] is None
    assert body["data"] is not None
    assert "ranking" in body["data"]
    assert isinstance(body["data"]["ranking"], list)
    assert len(body["data"]["ranking"]) == 6


def test_run_battle_missing_array_size(client):
    response = client.post("/api/run-battle", json={})
    assert response.status_code == 400

    body = response.get_json()
    assert body is not None
    assert body["success"] is False
    assert body["data"] is None
    assert body["error"] is not None
    assert body["error"]["code"] == "INVALID_REQUEST"
    assert body["error"]["message"] == "array_size is required"


def test_run_battle_invalid_array_size_type(client):
    response = client.post("/api/run-battle", json={"array_size": "abc"})
    assert response.status_code == 400

    body = response.get_json()
    assert body is not None
    assert body["success"] is False
    assert body["data"] is None
    assert body["error"] is not None
    assert body["error"]["code"] == "INVALID_REQUEST"
    assert body["error"]["message"] == "array_size must be integer"


def test_run_battle_array_size_out_of_range(client):
    response = client.post("/api/run-battle", json={"array_size": 5})
    assert response.status_code == 400

    body = response.get_json()
    assert body is not None
    assert body["success"] is False
    assert body["data"] is None
    assert body["error"] is not None
    assert body["error"]["code"] == "INVALID_REQUEST"
    assert body["error"]["message"] == "array_size must be between 10 and 1000000"