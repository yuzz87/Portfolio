from app.db.mysql_pool import get_conn


def test_db_connection():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT 1")
    row = cur.fetchone()
    cur.close()
    conn.close()

    assert row[0] == 1