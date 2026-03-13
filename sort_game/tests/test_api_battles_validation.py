def test_post_battles_duplicate_algorithm(client):
    invalid_results = [
        {"algorithm": "quick", "duration_ms": 0.057803, "rank": 1},
        {"algorithm": "quick", "duration_ms": 0.083504, "rank": 2},
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
    assert body["error"]["message"] == "duplicate algorithm: quick"


def test_post_battles_invalid_algorithm(client):
    invalid_results = [
        {"algorithm": "radix", "duration_ms": 0.057803, "rank": 1},
        {"algorithm": "merge", "duration_ms": 0.083504, "rank": 2},
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
    assert body["error"]["message"] == "results[0].algorithm is invalid: radix"


def test_post_battles_negative_duration(client):
    invalid_results = [
        {"algorithm": "quick", "duration_ms": -0.1, "rank": 1},
        {"algorithm": "merge", "duration_ms": 0.083504, "rank": 2},
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
    assert body["error"]["message"] == "results[0].duration_ms must be >= 0"


def test_post_battles_invalid_rank_range(client):
    invalid_results = [
        {"algorithm": "quick", "duration_ms": 0.057803, "rank": 1},
        {"algorithm": "merge", "duration_ms": 0.083504, "rank": 2},
        {"algorithm": "heap", "duration_ms": 0.084304, "rank": 3},
        {"algorithm": "insertion", "duration_ms": 0.242710, "rank": 4},
        {"algorithm": "selection", "duration_ms": 3.487550, "rank": 5},
        {"algorithm": "bubble", "duration_ms": 5.904760, "rank": 7},
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
    assert body["error"]["message"] == "results[5].rank must be between 1 and 6"


def test_post_battles_results_not_array(client):
    payload = {
        "array_size": 40,
        "benchmark_size": 2000,
        "results": "invalid",
    }

    response = client.post("/api/battles", json=payload)
    assert response.status_code == 400

    body = response.get_json()
    assert body is not None
    assert body["success"] is False
    assert body["data"] is None
    assert body["error"] is not None
    assert body["error"]["code"] == "INVALID_REQUEST"
    assert body["error"]["message"] == "results must be array"