def test_get_battles_limit_min(client, valid_results):
    save_payload = {
        "user_id": None,
        "array_size": 40,
        "benchmark_size": 2000,
        "results": valid_results,
    }
    client.post("/api/battles", json=save_payload)

    response = client.get("/api/battles?limit=1")
    assert response.status_code == 200


def test_get_battles_limit_max(client, valid_results):
    save_payload = {
        "user_id": None,
        "array_size": 40,
        "benchmark_size": 2000,
        "results": valid_results,
    }
    client.post("/api/battles", json=save_payload)

    response = client.get("/api/battles?limit=50")
    assert response.status_code == 200


def test_get_statistics_limit_min(client):
    response = client.get("/api/statistics?limit=1")
    assert response.status_code == 200


def test_get_statistics_limit_max(client):
    response = client.get("/api/statistics?limit=1000")
    assert response.status_code == 200