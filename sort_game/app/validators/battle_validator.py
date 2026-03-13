import math


ALLOWED_ALGORITHMS = {
    "bubble",
    "selection",
    "insertion",
    "merge",
    "quick",
    "heap",
}


def validate_battle_payload(payload: dict):
    if not isinstance(payload, dict):
        return False, "INVALID_INPUT", "payload must be an object"

    user_id = payload.get("user_id")
    array_size = payload.get("array_size")
    benchmark_size = payload.get("benchmark_size")
    results = payload.get("results")

    # user_id
    if user_id is not None:
        if type(user_id) is not int:
            return False, "INVALID_USER_ID", "user_id must be int or null"
        if user_id <= 0:
            return False, "INVALID_USER_ID", "user_id must be positive"

    # array_size
    if type(array_size) is not int:
        return False, "INVALID_ARRAY_SIZE", "array_size must be int"

    if not (5 <= array_size <= 100):
        return False, "INVALID_ARRAY_SIZE", "array_size must be between 5 and 100"

    # benchmark_size
    if type(benchmark_size) is not int:
        return False, "INVALID_BENCHMARK_SIZE", "benchmark_size must be int"

    if not (100 <= benchmark_size <= 1000000):
        return False, "INVALID_BENCHMARK_SIZE", "benchmark_size must be between 100 and 1000000"

    # results
    if not isinstance(results, list):
        return False, "INVALID_RESULTS", "results must be an array"

    if len(results) != 6:
        return False, "INVALID_RESULTS", "results must contain exactly 6 items"

    ranks = []
    algorithms = []

    for i, row in enumerate(results):
        if not isinstance(row, dict):
            return False, "INVALID_RESULTS", f"results[{i}] must be object"

        algorithm = row.get("algorithm")
        duration_ms = row.get("duration_ms")
        rank = row.get("rank")

        if not isinstance(algorithm, str):
            return False, "INVALID_ALGORITHM", f"results[{i}].algorithm must be string"

        if algorithm not in ALLOWED_ALGORITHMS:
            return False, "INVALID_ALGORITHM", f"results[{i}].algorithm is invalid: {algorithm}"

        if not isinstance(duration_ms, (int, float)) or isinstance(duration_ms, bool):
            return False, "INVALID_DURATION", f"results[{i}].duration_ms must be number"

        if duration_ms < 0 or not math.isfinite(duration_ms):
            return False, "INVALID_DURATION", f"results[{i}].duration_ms must be finite and >= 0"

        if type(rank) is not int:
            return False, "INVALID_RANK", f"results[{i}].rank must be int"

        if not (1 <= rank <= 6):
            return False, "INVALID_RANK", f"results[{i}].rank must be between 1 and 6"

        algorithms.append(algorithm)
        ranks.append(rank)

    if len(algorithms) != len(set(algorithms)):
        return False, "DUPLICATE_ALGORITHM", "algorithm must be unique"

    if len(ranks) != len(set(ranks)):
        return False, "DUPLICATE_RANK", "rank must be unique"

    if set(ranks) != set(range(1, len(results) + 1)):
        return False, "INVALID_RANK", "rank must be sequential from 1"

    return True, None, None