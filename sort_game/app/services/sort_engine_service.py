import json
import os
import subprocess
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[2]
DEFAULT_ENGINE_PATH = BASE_DIR / "cpp_engine" / "sort_engine"
ENGINE_PATH = Path(os.getenv("ENGINE_PATH", str(DEFAULT_ENGINE_PATH))).resolve()

ALGORITHM_ID_MAP = {
    "bubble": 1,
    "selection": 2,
    "insertion": 3,
    "merge": 4,
    "quick": 5,
    "heap": 6,
}


def run_sort(algorithm: str, size: int, seed: int | None = None) -> dict:
    if algorithm not in ALGORITHM_ID_MAP:
        raise ValueError(f"unknown algorithm: {algorithm}")

    if type(size) is not int:
        raise ValueError("size must be int")

    if size <= 0:
        raise ValueError("size must be positive")

    if seed is not None and type(seed) is not int:
        raise ValueError("seed must be int")

    if not ENGINE_PATH.exists():
        raise RuntimeError("sort_engine not found")

    cmd = [str(ENGINE_PATH), algorithm, str(size)]

    if seed is not None:
        cmd.append(str(seed))

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True,
            timeout=10,
        )
    except subprocess.TimeoutExpired as exc:
        raise RuntimeError("sort_engine execution timed out") from exc
    except subprocess.CalledProcessError as exc:
        raise RuntimeError("sort_engine execution failed") from exc

    try:
        data = json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        raise RuntimeError("invalid JSON from sort_engine") from exc

    if not isinstance(data, dict):
        raise RuntimeError("invalid response from sort_engine")

    returned_algorithm = data.get("algorithm")
    returned_size = data.get("size")
    duration_ms = data.get("duration_ms")

    if returned_algorithm not in ALGORITHM_ID_MAP:
        raise RuntimeError("invalid algorithm returned from sort_engine")

    if returned_algorithm != algorithm:
        raise RuntimeError("unexpected algorithm returned from sort_engine")

    try:
        parsed_size = int(returned_size)
    except (TypeError, ValueError) as exc:
        raise RuntimeError("invalid size returned from sort_engine") from exc

    try:
        parsed_duration = float(duration_ms)
    except (TypeError, ValueError) as exc:
        raise RuntimeError("invalid duration returned from sort_engine") from exc

    if parsed_size != size:
        raise RuntimeError("unexpected size returned from sort_engine")

    if parsed_duration < 0:
        raise RuntimeError("duration must be non-negative")

    return {
        "algorithm": returned_algorithm,
        "algorithm_id": ALGORITHM_ID_MAP[returned_algorithm],
        "size": parsed_size,
        "duration_ms": parsed_duration,
    }