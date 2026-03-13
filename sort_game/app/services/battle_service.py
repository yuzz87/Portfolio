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


# =====================================
# C++ソートランキング実行
# =====================================
def run_battle(array_size: int) -> List[Dict[str, Any]]:
    if type(array_size) is not int:
        raise ValueError("array_size must be int")

    if not (10 <= array_size <= 1000000):
        raise ValueError("array_size must be between 10 and 1000000")

    results: List[Dict[str, Any]] = []

    for algo in ALGORITHMS:
        raw = run_sort(algo, array_size)

        if not isinstance(raw, dict):
            raise ValueError(f"run_sort returned invalid result for {algo}")

        algorithm = raw.get("algorithm")
        duration_ms = raw.get("duration_ms")

        if algorithm != algo:
            raise ValueError(f"run_sort returned unexpected algorithm: {algorithm}")

        try:
            duration_ms = float(duration_ms)
        except (TypeError, ValueError):
            raise ValueError(f"invalid duration_ms returned for {algo}")

        if not math.isfinite(duration_ms) or duration_ms < 0:
            raise ValueError(f"duration_ms must be finite and >= 0 for {algo}")

        results.append({
            "algorithm": algorithm,
            "duration_ms": duration_ms,
        })

    results.sort(key=lambda x: x["duration_ms"])

    for i, row in enumerate(results, start=1):
        row["rank"] = i

    return results


# =====================================
# バトル保存
# =====================================
def save_battle_result(
    user_id: int | None,
    array_size: int,
    benchmark_size: int,
    results: List[Dict[str, Any]],
):
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

    for i, row in enumerate(results):
        if not isinstance(row, dict):
            raise ValueError(f"results[{i}] must be object")

        algorithm = row.get("algorithm")
        duration_ms = row.get("duration_ms")
        rank = row.get("rank")

        if algorithm not in ALGORITHMS:
            raise ValueError(f"results[{i}].algorithm is invalid: {algorithm}")

        try:
            duration_ms = float(duration_ms)
        except (TypeError, ValueError):
            raise ValueError(f"results[{i}].duration_ms must be number")

        if not math.isfinite(duration_ms) or duration_ms < 0:
            raise ValueError(f"results[{i}].duration_ms must be finite and >= 0")

        if type(rank) is not int:
            raise ValueError(f"results[{i}].rank must be int")

        if not (1 <= rank <= len(ALGORITHMS)):
            raise ValueError(f"results[{i}].rank must be between 1 and 6")

        if algorithm in seen_algorithms:
            raise ValueError(f"duplicate algorithm: {algorithm}")
        seen_algorithms.add(algorithm)

        if rank in seen_ranks:
            raise ValueError(f"duplicate rank: {rank}")
        seen_ranks.add(rank)

        normalized_results.append({
            "algorithm": algorithm,
            "duration_ms": duration_ms,
            "rank": rank,
        })

    if seen_ranks != set(range(1, len(ALGORITHMS) + 1)):
        raise ValueError("rank must be sequential from 1 to 6")

    normalized_results.sort(key=lambda x: x["rank"])

    return save_battle(
        user_id=user_id,
        array_size=array_size,
        benchmark_size=benchmark_size,
        results=normalized_results,
    )


# =====================================
# バトル履歴取得
# =====================================
def list_battles(limit: int = 10):
    if type(limit) is not int:
        raise ValueError("limit must be int")

    if not (1 <= limit <= 50):
        raise ValueError("limit must be between 1 and 50")

    return fetch_recent_battles(limit)


# =====================================
# 統計取得
# =====================================
def get_statistics(limit: int = 10):
    if type(limit) is not int:
        raise ValueError("limit must be int")

    if not (1 <= limit <= 1000):
        raise ValueError("limit must be between 1 and 1000")

    rows = fetch_statistics(limit)

    stats: Dict[str, Dict[str, Any]] = {}

    for row in rows:
        algorithm = row.get("algorithm")
        if algorithm not in ALGORITHMS:
            continue

        plays = int(row.get("plays") or 0)
        wins = int(row.get("wins") or 0)
        avg = float(row.get("avg_duration_ms") or 0.0)

        win_rate = (wins / plays) if plays > 0 else 0.0

        stats[algorithm] = {
            "avg_duration_ms": avg,
            "win_rate": win_rate,
            "wins": wins,
            "plays": plays,
        }

    return stats