def test_post_battles_invalid_benchmark_size_type(client, valid_results):
    payload = {
        "array_size": 40,
        "benchmark_size": "abc",
        "results": valid_results,
    }

    response = client.post("/api/battles", json=payload)
    assert response.status_code == 400

    body = response.get_json()
    assert body["success"] is False
    assert body["data"] is None
    assert body["error"]["code"] == "INVALID_REQUEST"


def test_post_battles_benchmark_size_out_of_range_low(client, valid_results):
    payload = {
        "array_size": 40,
        "benchmark_size": 99,
        "results": valid_results,
    }

    response = client.post("/api/battles", json=payload)
    assert response.status_code == 400

    body = response.get_json()
    assert body["success"] is False
    assert body["data"] is None
    assert body["error"]["code"] == "INVALID_REQUEST"


def test_post_battles_benchmark_size_out_of_range_high(client, valid_results):
    payload = {
        "array_size": 40,
        "benchmark_size": 10001,
        "results": valid_results,
    }

    response = client.post("/api/battles", json=payload)
    assert response.status_code == 400

    body = response.get_json()
    assert body["success"] is False
    assert body["data"] is None
    assert body["error"]["code"] == "INVALID_REQUEST"