def test_get_battles_invalid_limit_string(client):
    response = client.get("/api/battles?limit=abc")
    assert response.status_code == 400

    body = response.get_json()
    assert body is not None
    assert body["success"] is False
    assert body["data"] is None
    assert body["error"] is not None
    assert body["error"]["code"] == "INVALID_REQUEST"
    assert body["error"]["message"] == "limit must be integer"


def test_get_battles_invalid_limit_zero(client):
    response = client.get("/api/battles?limit=0")
    assert response.status_code == 400

    body = response.get_json()
    assert body is not None
    assert body["success"] is False
    assert body["data"] is None
    assert body["error"] is not None
    assert body["error"]["code"] == "INVALID_REQUEST"
    assert body["error"]["message"] == "limit must be between 1 and 50"


def test_get_battles_invalid_limit_over_max(client):
    response = client.get("/api/battles?limit=51")
    assert response.status_code == 400

    body = response.get_json()
    assert body is not None
    assert body["success"] is False
    assert body["data"] is None
    assert body["error"] is not None
    assert body["error"]["code"] == "INVALID_REQUEST"
    assert body["error"]["message"] == "limit must be between 1 and 50"