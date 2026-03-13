from flask import Blueprint, request, jsonify

from ..services.battle_service import (
    run_battle,
    list_battles,
    get_statistics,
    save_battle_result,
)

api_bp = Blueprint("api", __name__, url_prefix="/api")


def ok(data, status=200):
    return jsonify({
        "success": True,
        "data": data,
        "error": None
    }), status


def ng(code, message, status=400):
    return jsonify({
        "success": False,
        "data": None,
        "error": {
            "code": code,
            "message": message
        }
    }), status


def parse_json_body():
    data = request.get_json(silent=True)
    if data is None:
        return None, ng("INVALID_JSON", "JSON body is required", 400)
    if not isinstance(data, dict):
        return None, ng("INVALID_REQUEST", "JSON body must be object", 400)
    return data, None


def validate_optional_user_id(user_id):
    if user_id is None:
        return None, None

    if isinstance(user_id, bool):
        return None, "user_id must be integer or null"

    try:
        parsed_user_id = int(user_id)
    except (TypeError, ValueError):
        return None, "user_id must be integer or null"

    if parsed_user_id < 1:
        return None, "user_id must be positive integer"

    return parsed_user_id, None


def validate_battle_results(results):
    if not isinstance(results, list):
        return "results must be array"

    if len(results) != 6:
        return "results must contain exactly 6 items"

    allowed_algorithms = {
        "bubble", "selection", "insertion", "merge", "quick", "heap"
    }

    seen_algorithms = set()
    seen_ranks = set()

    for i, row in enumerate(results):
        if not isinstance(row, dict):
            return f"results[{i}] must be object"

        for key in ("algorithm", "duration_ms", "rank"):
            if key not in row:
                return f"results[{i}].{key} is required"

        algorithm = row["algorithm"]
        duration_ms = row["duration_ms"]
        rank = row["rank"]

        if not isinstance(algorithm, str):
            return f"results[{i}].algorithm must be string"

        if algorithm not in allowed_algorithms:
            return f"results[{i}].algorithm is invalid: {algorithm}"

        if not isinstance(duration_ms, (int, float)) or isinstance(duration_ms, bool):
            return f"results[{i}].duration_ms must be number"

        if duration_ms < 0:
            return f"results[{i}].duration_ms must be >= 0"

        if not isinstance(rank, int) or isinstance(rank, bool):
            return f"results[{i}].rank must be integer"

        if rank < 1 or rank > 6:
            return f"results[{i}].rank must be between 1 and 6"

        if algorithm in seen_algorithms:
            return f"duplicate algorithm: {algorithm}"
        seen_algorithms.add(algorithm)

        if rank in seen_ranks:
            return f"duplicate rank: {rank}"
        seen_ranks.add(rank)

    return None


@api_bp.route("/run-battle", methods=["POST"])
def run_battle_api():
    data, error_response = parse_json_body()
    if error_response:
        return error_response

    if "array_size" not in data:
        return ng("INVALID_REQUEST", "array_size is required", 400)

    try:
        array_size = int(data["array_size"])
    except (TypeError, ValueError):
        return ng("INVALID_REQUEST", "array_size must be integer", 400)

    if array_size < 10 or array_size > 1000000:
        return ng("INVALID_REQUEST", "array_size must be between 10 and 1000000", 400)

    try:
        ranking = run_battle(array_size)
        return ok({"ranking": ranking})
    except ValueError as e:
        return ng("INVALID_REQUEST", str(e), 400)
    except Exception:
        return ng("INTERNAL_ERROR", "internal server error", 500)


@api_bp.route("/battles", methods=["POST"])
def save_battle_api():
    data, error_response = parse_json_body()
    if error_response:
        return error_response

    required_fields = ("array_size", "benchmark_size", "results")
    for field in required_fields:
        if field not in data:
            return ng("INVALID_REQUEST", f"{field} is required", 400)

    try:
        array_size = int(data["array_size"])
        benchmark_size = int(data["benchmark_size"])
    except (TypeError, ValueError):
        return ng(
            "INVALID_REQUEST",
            "array_size and benchmark_size must be integer",
            400
        )

    if array_size < 5 or array_size > 1000:
        return ng("INVALID_REQUEST", "array_size must be between 5 and 1000", 400)

    if benchmark_size < 100 or benchmark_size > 10000:
        return ng("INVALID_REQUEST", "benchmark_size must be between 100 and 10000", 400)

    user_id, user_id_error = validate_optional_user_id(data.get("user_id"))
    if user_id_error:
        return ng("INVALID_REQUEST", user_id_error, 400)

    results = data["results"]
    validation_error = validate_battle_results(results)
    if validation_error:
        return ng("INVALID_REQUEST", validation_error, 400)

    try:
        battle_id = save_battle_result(
            user_id=user_id,
            array_size=array_size,
            benchmark_size=benchmark_size,
            results=results
        )
        return ok({"battle_id": battle_id}, 201)
    except ValueError as e:
        return ng("INVALID_REQUEST", str(e), 400)
    except Exception:
        return ng("INTERNAL_ERROR", "internal server error", 500)


@api_bp.route("/battles", methods=["GET"])
def list_battles_api():
    raw_limit = request.args.get("limit", "10")

    try:
        limit = int(raw_limit)
    except (TypeError, ValueError):
        return ng("INVALID_REQUEST", "limit must be integer", 400)

    if limit < 1 or limit > 50:
        return ng("INVALID_REQUEST", "limit must be between 1 and 50", 400)

    try:
        data = list_battles(limit)
        return ok(data)
    except ValueError as e:
        return ng("INVALID_REQUEST", str(e), 400)
    except Exception:
        return ng("INTERNAL_ERROR", "internal server error", 500)


@api_bp.route("/statistics", methods=["GET"])
def statistics_api():
    raw_limit = request.args.get("limit", "10")

    try:
        limit = int(raw_limit)
    except (TypeError, ValueError):
        return ng("INVALID_REQUEST", "limit must be integer", 400)

    if limit < 1 or limit > 1000:
        return ng("INVALID_REQUEST", "limit must be between 1 and 1000", 400)

    try:
        stats = get_statistics(limit)
        return ok(stats)
    except ValueError as e:
        return ng("INVALID_REQUEST", str(e), 400)
    except Exception:
        return ng("INTERNAL_ERROR", "internal server error", 500)