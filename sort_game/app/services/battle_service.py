from __future__ import annotations

import math
from typing import Any, Dict, List

from .sort_engine_service import run_sort
from ..repositories.battle_repository import (
    save_battle,
    fetch_recent_battles,
    fetch_statistics,
)

ALGORITHMS = (
    "bubble",
    "selection",
    "insertion",
    "merge",
    "quick",
    "heap",
)


def run_battle(array_size: int) -> List[Dict[str, Any]]:
    if type(array_size) is not int:
        raise ValueError("array_size must be int")

    if not (10 <= array_size <= 1_000_000):
        raise ValueError("array_size must be between 10 and 1000000")

    results: List[Dict[str, Any]] = []

    for algorithm_name in ALGORITHMS:
        raw = run_sort(algorithm_name, array_size)

        if not isinstance(raw, dict):
            raise ValueError(f"run_sort returned invalid result for {algorithm_name}")

        returned_algorithm = raw.get("algorithm")
        duration_ms = raw.get("duration_ms")

        if returned_algorithm != algorithm_name:
            raise ValueError(
                f"run_sort returned unexpected algorithm: {returned_algorithm}"
            )

        try:
            parsed_duration = float(duration_ms)
        except (TypeError, ValueError):
            raise ValueError(f"invalid duration_ms returned for {algorithm_name}")

        if not math.isfinite(parsed_duration) or parsed_duration < 0:
            raise ValueError(
                f"duration_ms must be finite and >= 0 for {algorithm_name}"
            )

        results.append({
            "algorithm": returned_algorithm,
            "duration_ms": parsed_duration,
        })

    results.sort(key=lambda row: row["duration_ms"])

    for index, row in enumerate(results, start=1):
        row["rank"] = index

    return results


def save_battle_result(
    user_id: int | None,
    array_size: int,
    benchmark_size: int,
    results: List[Dict[str, Any]],
) -> int:
    if user_id is not None:
        if type(user_id) is not int or user_id <= 0:
            raise ValueError("user_id must be positive int or null")

    if type(array_size) is not int:
        raise ValueError("array_size must be int")

    if not (5 <= array_size <= 1000):
        raise ValueError("array_size must be between 5 and 1000")

    if type(benchmark_size) is not int:
        raise ValueError("benchmark_size must be int")

    if not (100 <= benchmark_size <= 10000):
        raise ValueError("benchmark_size must be between 100 and 10000")

    if not isinstance(results, list):
        raise ValueError("results must be array")

    if len(results) != len(ALGORITHMS):
        raise ValueError("results must contain exactly 6 items")

    normalized_results: List[Dict[str, Any]] = []
    seen_algorithms = set()
    seen_ranks = set()

    for index, row in enumerate(results):
        if not isinstance(row, dict):
            raise ValueError(f"results[{index}] must be object")

        algorithm = row.get("algorithm")
        duration_ms = row.get("duration_ms")
        rank = row.get("rank")

        if algorithm not in ALGORITHMS:
            raise ValueError(f"results[{index}].algorithm is invalid: {algorithm}")

        try:
            parsed_duration = float(duration_ms)
        except (TypeError, ValueError):
            raise ValueError(f"results[{index}].duration_ms must be number")

        if not math.isfinite(parsed_duration) or parsed_duration < 0:
            raise ValueError(
                f"results[{index}].duration_ms must be finite and >= 0"
            )

        if type(rank) is not int:
            raise ValueError(f"results[{index}].rank must be int")

        if not (1 <= rank <= len(ALGORITHMS)):
            raise ValueError(
                f"results[{index}].rank must be between 1 and {len(ALGORITHMS)}"
            )

        if algorithm in seen_algorithms:
            raise ValueError(f"duplicate algorithm: {algorithm}")
        seen_algorithms.add(algorithm)

        if rank in seen_ranks:
            raise ValueError(f"duplicate rank: {rank}")
        seen_ranks.add(rank)

        normalized_results.append({
            "algorithm": algorithm,
            "duration_ms": parsed_duration,
            "rank": rank,
        })

    expected_ranks = set(range(1, len(ALGORITHMS) + 1))
    if seen_ranks != expected_ranks:
        raise ValueError("rank must be sequential from 1 to 6")

    normalized_results.sort(key=lambda row: row["rank"])

    return save_battle(
        user_id=user_id,
        array_size=array_size,
        benchmark_size=benchmark_size,
        results=normalized_results,
    )


def list_battles(limit: int = 10) -> List[Dict[str, Any]]:
    if type(limit) is not int:
        raise ValueError("limit must be int")

    if not (1 <= limit <= 50):
        raise ValueError("limit must be between 1 and 50")

    return fetch_recent_battles(limit)


def get_statistics(limit: int = 10) -> Dict[str, Dict[str, Any]]:
    if type(limit) is not int:
        raise ValueError("limit must be int")

    if not (1 <= limit <= 1000):
        raise ValueError("limit must be between 1 and 1000")

    rows = fetch_statistics(limit)

    stats: Dict[str, Dict[str, Any]] = {
        algorithm: {
            "avg_duration_ms": 0.0,
            "win_rate": 0.0,
            "wins": 0,
            "plays": 0,
        }
        for algorithm in ALGORITHMS
    }

    for row in rows:
        algorithm = row.get("algorithm")
        if algorithm not in ALGORITHMS:
            continue

        plays = int(row.get("plays") or 0)
        wins = int(row.get("wins") or 0)
        avg_duration_ms = float(row.get("avg_duration_ms") or 0.0)
        win_rate = (wins / plays) if plays > 0 else 0.0

        stats[algorithm] = {
            "avg_duration_ms": avg_duration_ms,
            "win_rate": win_rate,
            "wins": wins,
            "plays": plays,
        }

    return stats