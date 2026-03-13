def test_get_statistics_success(client):
    response = client.get("/api/statistics")

    assert response.status_code == 200

    body = response.get_json()
    assert body is not None
    assert body["success"] is True
    assert body["error"] is None
    assert body["data"] is not None
    assert isinstance(body["data"], dict)


def test_get_statistics_contains_data_after_battle_save(client, valid_results):
    save_payload = {
        "user_id": None,
        "array_size": 40,
        "benchmark_size": 2000,
        "results": valid_results,
    }

    save_response = client.post("/api/battles", json=save_payload)
    assert save_response.status_code == 201

    response = client.get("/api/statistics")
    assert response.status_code == 200

    body = response.get_json()
    assert body is not None
    assert body["success"] is True
    assert body["error"] is None

    data = body["data"]
    assert isinstance(data, dict)
    assert len(data) > 0

    assert "quick" in data
    assert "wins" in data["quick"]
    assert "plays" in data["quick"]
    assert "win_rate" in data["quick"]
    assert "avg_duration_ms" in data["quick"]