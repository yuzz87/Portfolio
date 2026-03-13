import logging
import time

import mysql.connector
from mysql.connector import pooling

from app.config import Config

logger = logging.getLogger(__name__)

_pool = None


def _create_pool():
    Config.validate()

    return pooling.MySQLConnectionPool(
        pool_name="sort_portfolio_pool",
        pool_size=10,
        pool_reset_session=True,
        host=Config.DB_HOST,
        port=Config.DB_PORT,
        user=Config.DB_USER,
        password=Config.DB_PASSWORD,
        database=Config.DB_NAME,
        charset="utf8mb4",
        autocommit=False,
        connect_timeout=5,
    )


def get_conn():
    global _pool

    if _pool is None:
        retries = 5

        for _ in range(retries):
            try:
                _pool = _create_pool()
                logger.info("MySQL connection pool created")
                break
            except mysql.connector.Error:
                logger.warning("MySQL connection failed")
                time.sleep(2)
        else:
            raise RuntimeError("MySQL connection failed after retries")

    try:
        conn = _pool.get_connection()
        conn.set_charset_collation("utf8mb4", "utf8mb4_unicode_ci")
        return conn
    except mysql.connector.Error as exc:
        raise RuntimeError("Failed to get MySQL connection from pool") from exc