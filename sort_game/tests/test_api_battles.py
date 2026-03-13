def test_post_battles_success(client, valid_results):
    payload = {
        "user_id": None,
        "array_size": 40,
        "benchmark_size": 2000,
        "results": valid_results,
    }

    response = client.post("/api/battles", json=payload)

    assert response.status_code == 201

    body = response.get_json()
    assert body is not None
    assert body["success"] is True
    assert body["error"] is None
    assert body["data"] is not None
    assert "battle_id" in body["data"]
    assert isinstance(body["data"]["battle_id"], int)


def test_post_battles_missing_results(client):
    payload = {
        "array_size": 40,
        "benchmark_size": 2000,
    }

    response = client.post("/api/battles", json=payload)

    assert response.status_code == 400

    body = response.get_json()
    assert body is not None
    assert body["success"] is False
    assert body["data"] is None
    assert body["error"] is not None
    assert body["error"]["code"] == "INVALID_REQUEST"


def test_post_battles_invalid_result_count(client, valid_results):
    payload = {
        "array_size": 40,
        "benchmark_size": 2000,
        "results": valid_results[:5],
    }

    response = client.post("/api/battles", json=payload)

    assert response.status_code == 400

    body = response.get_json()
    assert body is not None
    assert body["success"] is False
    assert body["data"] is None
    assert body["error"] is not None
    assert body["error"]["code"] == "INVALID_REQUEST"
    assert body["error"]["message"] == "results must contain exactly 6 items"


def test_post_battles_duplicate_rank(client):
    invalid_results = [
        {"algorithm": "quick", "duration_ms": 0.057803, "rank": 1},
        {"algorithm": "merge", "duration_ms": 0.083504, "rank": 1},
        {"algorithm": "heap", "duration_ms": 0.084304, "rank": 3},
        {"algorithm": "insertion", "duration_ms": 0.242710, "rank": 4},
        {"algorithm": "selection", "duration_ms": 3.487550, "rank": 5},
        {"algorithm": "bubble", "duration_ms": 5.904760, "rank": 6},
    ]

    payload = {
        "array_size": 40,
        "benchmark_size": 2000,
        "results": invalid_results,
    }

    response = client.post("/api/battles", json=payload)

    assert response.status_code == 400

    body = response.get_json()
    assert body is not None
    assert body["success"] is False
    assert body["data"] is None
    assert body["error"] is not None
    assert body["error"]["code"] == "INVALID_REQUEST"
    assert body["error"]["message"] == "duplicate rank: 1"