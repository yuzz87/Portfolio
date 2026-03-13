from unittest.mock import patch
import pytest

from app.db import mysql_pool


def test_get_conn_pool_creation_failure():
    original_pool = mysql_pool._pool
    mysql_pool._pool = None

    try:
        with patch("app.db.mysql_pool.pooling.MySQLConnectionPool") as mock_pool:
            mock_pool.side_effect = Exception("pool create failed")

            with pytest.raises(Exception):
                mysql_pool.get_conn()
    finally:
        mysql_pool._pool = original_pool


def test_get_conn_connection_failure():
    class DummyPool:
        def get_connection(self):
            raise Exception("connection failed")

    original_pool = mysql_pool._pool
    mysql_pool._pool = None

    try:
        with patch("app.db.mysql_pool.pooling.MySQLConnectionPool", return_value=DummyPool()):
            with pytest.raises(Exception):
                mysql_pool.get_conn()
    finally:
        mysql_pool._pool = original_pool