def test_get_battles_success(client, valid_results):
    save_payload = {
        "user_id": None,
        "array_size": 40,
        "benchmark_size": 2000,
        "results": valid_results,
    }

    save_response = client.post("/api/battles", json=save_payload)
    assert save_response.status_code == 201

    response = client.get("/api/battles?limit=10")
    assert response.status_code == 200

    body = response.get_json()
    assert body is not None
    assert body["success"] is True
    assert body["error"] is None
    assert isinstance(body["data"], list)
    assert len(body["data"]) > 0

    row = body["data"][0]
    assert "battle_id" in row
    assert "algorithm" in row
    assert "duration_ms" in row
    assert "rank" in row