import subprocess
import json
import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[2]
DEFAULT_ENGINE_PATH = BASE_DIR / "cpp_engine" / "sort_engine"

ENGINE_PATH = os.getenv("ENGINE_PATH", str(DEFAULT_ENGINE_PATH))


ALGORITHM_ID_MAP = {
    "bubble": 1,
    "selection": 2,
    "insertion": 3,
    "merge": 4,
    "quick": 5,
    "heap": 6,
}


def run_sort(algorithm: str, size: int, seed: int | None = None):

    if algorithm not in ALGORITHM_ID_MAP:
        raise ValueError(f"Unknown algorithm: {algorithm}")

    if not os.path.exists(ENGINE_PATH):
        raise RuntimeError(f"sort_engine not found: {ENGINE_PATH}")

    cmd = [ENGINE_PATH, algorithm, str(size)]

    if seed is not None:
        cmd.append(str(seed))

    try:

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True
        )

    except subprocess.CalledProcessError as e:

        raise RuntimeError(
            f"sort_engine execution failed: {e.stderr}"
        )

    try:

        data = json.loads(result.stdout)

    except json.JSONDecodeError:

        raise RuntimeError(
            f"Invalid JSON from sort_engine: {result.stdout}"
        )

    return {
        "algorithm": data["algorithm"],
        "algorithm_id": ALGORITHM_ID_MAP[data["algorithm"]],
        "size": data["size"],
        "duration_ms": float(data["duration_ms"])
    }