def test_get_battles_empty(client):
    response = client.get("/api/battles")
    assert response.status_code == 200

    body = response.get_json()
    assert body is not None
    assert body["success"] is True
    assert body["error"] is None
    assert isinstance(body["data"], list)
    assert len(body["data"]) == 0


def test_get_statistics_empty(client):
    response = client.get("/api/statistics")
    assert response.status_code == 200

    body = response.get_json()
    assert body is not None
    assert body["success"] is True
    assert body["error"] is None
    assert isinstance(body["data"], dict)