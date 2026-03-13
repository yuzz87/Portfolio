import os
import sys
from pathlib import Path

import pytest

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from app import create_app
from app.db.mysql_pool import get_conn


@pytest.fixture(scope="session")
def app():
    os.environ["FLASK_ENV"] = "testing"
    os.environ.setdefault("DB_HOST", "127.0.0.1")
    os.environ.setdefault("DB_PORT", "3306")
    os.environ.setdefault("DB_NAME", "test_db")
    os.environ.setdefault("DB_USER", "test_user")
    os.environ.setdefault("DB_PASSWORD", "test_password")

    app = create_app()
    app.config.update(TESTING=True)
    return app


@pytest.fixture(scope="session")
def client(app):
    return app.test_client()


@pytest.fixture
def valid_results():
    return [
        {"algorithm": "quick", "duration_ms": 0.057803, "rank": 1},
        {"algorithm": "merge", "duration_ms": 0.083504, "rank": 2},
        {"algorithm": "heap", "duration_ms": 0.084304, "rank": 3},
        {"algorithm": "insertion", "duration_ms": 0.242710, "rank": 4},
        {"algorithm": "selection", "duration_ms": 3.487550, "rank": 5},
        {"algorithm": "bubble", "duration_ms": 5.904760, "rank": 6},
    ]


@pytest.fixture(autouse=True)
def clean_tables():
    conn = get_conn()
    cur = conn.cursor()

    try:
        cur.execute("DELETE FROM battle_results")
        cur.execute("DELETE FROM battles")
        conn.commit()
        yield
    finally:
        cur.close()
        conn.close()