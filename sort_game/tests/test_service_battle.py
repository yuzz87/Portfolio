import math
from unittest.mock import patch

import pytest

from app.services.battle_service import (
    run_battle,
    save_battle_result,
    list_battles,
    get_statistics,
)


def test_run_battle_invalid_array_size_type():
    with pytest.raises(ValueError) as exc_info:
        run_battle("100")  # type: ignore[arg-type]

    assert str(exc_info.value) == "array_size must be int"


def test_run_battle_array_size_out_of_range_low():
    with pytest.raises(ValueError) as exc_info:
        run_battle(9)

    assert str(exc_info.value) == "array_size must be between 10 and 1000000"


def test_run_battle_array_size_out_of_range_high():
    with pytest.raises(ValueError) as exc_info:
        run_battle(1000001)

    assert str(exc_info.value) == "array_size must be between 10 and 1000000"


def test_run_battle_invalid_result_type():
    with patch("app.services.battle_service.run_sort", return_value="invalid"):
        with pytest.raises(ValueError) as exc_info:
            run_battle(2000)

    assert "run_sort returned invalid result" in str(exc_info.value)


def test_run_battle_unexpected_algorithm():
    with patch("app.services.battle_service.run_sort") as mock_run:
        mock_run.return_value = {
            "algorithm": "wrong",
            "duration_ms": 0.1,
        }

        with pytest.raises(ValueError) as exc_info:
            run_battle(2000)

    assert "run_sort returned unexpected algorithm" in str(exc_info.value)


def test_run_battle_invalid_duration_type():
    with patch("app.services.battle_service.run_sort") as mock_run:
        mock_run.return_value = {
            "algorithm": "bubble",
            "duration_ms": "not-number",
        }

        with pytest.raises(ValueError) as exc_info:
            run_battle(2000)

    assert "invalid duration_ms returned" in str(exc_info.value)


def test_run_battle_invalid_duration_nan():
    with patch("app.services.battle_service.run_sort") as mock_run:
        mock_run.return_value = {
            "algorithm": "bubble",
            "duration_ms": math.nan,
        }

        with pytest.raises(ValueError) as exc_info:
            run_battle(2000)

    assert "duration_ms must be finite and >= 0" in str(exc_info.value)


def test_run_battle_invalid_duration_negative():
    with patch("app.services.battle_service.run_sort") as mock_run:
        mock_run.return_value = {
            "algorithm": "bubble",
            "duration_ms": -1,
        }

        with pytest.raises(ValueError) as exc_info:
            run_battle(2000)

    assert "duration_ms must be finite and >= 0" in str(exc_info.value)


def test_save_battle_result_invalid_user_id_zero(valid_results):
    with pytest.raises(ValueError) as exc_info:
        save_battle_result(
            user_id=0,
            array_size=40,
            benchmark_size=2000,
            results=valid_results,
        )

    assert str(exc_info.value) == "user_id must be positive int or null"


def test_save_battle_result_invalid_user_id_type(valid_results):
    with pytest.raises(ValueError) as exc_info:
        save_battle_result(
            user_id="1",  # type: ignore[arg-type]
            array_size=40,
            benchmark_size=2000,
            results=valid_results,
        )

    assert str(exc_info.value) == "user_id must be positive int or null"


def test_save_battle_result_invalid_array_size_type(valid_results):
    with pytest.raises(ValueError) as exc_info:
        save_battle_result(
            user_id=None,
            array_size="40",  # type: ignore[arg-type]
            benchmark_size=2000,
            results=valid_results,
        )

    assert str(exc_info.value) == "array_size must be int"


def test_save_battle_result_array_size_out_of_range_low(valid_results):
    with pytest.raises(ValueError) as exc_info:
        save_battle_result(
            user_id=None,
            array_size=4,
            benchmark_size=2000,
            results=valid_results,
        )

    assert str(exc_info.value) == "array_size must be between 5 and 1000"


def test_save_battle_result_array_size_out_of_range_high(valid_results):
    with pytest.raises(ValueError) as exc_info:
        save_battle_result(
            user_id=None,
            array_size=1001,
            benchmark_size=2000,
            results=valid_results,
        )

    assert str(exc_info.value) == "array_size must be between 5 and 1000"


def test_save_battle_result_invalid_benchmark_size_type(valid_results):
    with pytest.raises(ValueError) as exc_info:
        save_battle_result(
            user_id=None,
            array_size=40,
            benchmark_size="2000",  # type: ignore[arg-type]
            results=valid_results,
        )

    assert str(exc_info.value) == "benchmark_size must be int"


def test_save_battle_result_benchmark_size_out_of_range_low(valid_results):
    with pytest.raises(ValueError) as exc_info:
        save_battle_result(
            user_id=None,
            array_size=40,
            benchmark_size=99,
            results=valid_results,
        )

    assert str(exc_info.value) == "benchmark_size must be between 100 and 10000"


def test_save_battle_result_benchmark_size_out_of_range_high(valid_results):
    with pytest.raises(ValueError) as exc_info:
        save_battle_result(
            user_id=None,
            array_size=40,
            benchmark_size=10001,
            results=valid_results,
        )

    assert str(exc_info.value) == "benchmark_size must be between 100 and 10000"


def test_save_battle_result_results_not_array():
    with pytest.raises(ValueError) as exc_info:
        save_battle_result(
            user_id=None,
            array_size=40,
            benchmark_size=2000,
            results="invalid",  # type: ignore[arg-type]
        )

    assert str(exc_info.value) == "results must be array"


def test_save_battle_result_results_invalid_count(valid_results):
    with pytest.raises(ValueError) as exc_info:
        save_battle_result(
            user_id=None,
            array_size=40,
            benchmark_size=2000,
            results=valid_results[:5],
        )

    assert str(exc_info.value) == "results must contain exactly 6 items"


def test_save_battle_result_row_not_object():
    invalid_results = [
        "invalid",
        {"algorithm": "merge", "duration_ms": 0.2, "rank": 2},
        {"algorithm": "heap", "duration_ms": 0.3, "rank": 3},
        {"algorithm": "insertion", "duration_ms": 0.4, "rank": 4},
        {"algorithm": "selection", "duration_ms": 0.5, "rank": 5},
        {"algorithm": "bubble", "duration_ms": 0.6, "rank": 6},
    ]

    with pytest.raises(ValueError) as exc_info:
        save_battle_result(
            user_id=None,
            array_size=40,
            benchmark_size=2000,
            results=invalid_results,  # type: ignore[arg-type]
        )

    assert str(exc_info.value) == "results[0] must be object"


def test_save_battle_result_invalid_duration_number(valid_results):
    invalid_results = [dict(row) for row in valid_results]
    invalid_results[0]["duration_ms"] = "abc"

    with pytest.raises(ValueError) as exc_info:
        save_battle_result(
            user_id=None,
            array_size=40,
            benchmark_size=2000,
            results=invalid_results,
        )

    assert str(exc_info.value) == "results[0].duration_ms must be number"


def test_save_battle_result_invalid_duration_nan(valid_results):
    invalid_results = [dict(row) for row in valid_results]
    invalid_results[0]["duration_ms"] = math.nan

    with pytest.raises(ValueError) as exc_info:
        save_battle_result(
            user_id=None,
            array_size=40,
            benchmark_size=2000,
            results=invalid_results,
        )

    assert str(exc_info.value) == "results[0].duration_ms must be finite and >= 0"


def test_save_battle_result_invalid_rank_type(valid_results):
    invalid_results = [dict(row) for row in valid_results]
    invalid_results[0]["rank"] = "1"

    with pytest.raises(ValueError) as exc_info:
        save_battle_result(
            user_id=None,
            array_size=40,
            benchmark_size=2000,
            results=invalid_results,
        )

    assert str(exc_info.value) == "results[0].rank must be int"


def test_save_battle_result_non_sequential_rank(valid_results):
    invalid_results = [dict(row) for row in valid_results]
    invalid_results[0]["rank"] = 6
    invalid_results[5]["rank"] = 1

    with patch("app.services.battle_service.save_battle") as mock_save:
        mock_save.return_value = 1

        result = save_battle_result(
            user_id=None,
            array_size=40,
            benchmark_size=2000,
            results=invalid_results,
        )

    assert result == 1


def test_list_battles_invalid_limit_type():
    with pytest.raises(ValueError) as exc_info:
        list_battles("10")  # type: ignore[arg-type]

    assert str(exc_info.value) == "limit must be int"


def test_list_battles_invalid_limit_low():
    with pytest.raises(ValueError) as exc_info:
        list_battles(0)

    assert str(exc_info.value) == "limit must be between 1 and 50"


def test_list_battles_invalid_limit_high():
    with pytest.raises(ValueError) as exc_info:
        list_battles(51)

    assert str(exc_info.value) == "limit must be between 1 and 50"


def test_get_statistics_invalid_limit_type():
    with pytest.raises(ValueError) as exc_info:
        get_statistics("10")  # type: ignore[arg-type]

    assert str(exc_info.value) == "limit must be int"


def test_get_statistics_invalid_limit_low():
    with pytest.raises(ValueError) as exc_info:
        get_statistics(0)

    assert str(exc_info.value) == "limit must be between 1 and 1000"


def test_get_statistics_invalid_limit_high():
    with pytest.raises(ValueError) as exc_info:
        get_statistics(1001)

    assert str(exc_info.value) == "limit must be between 1 and 1000"