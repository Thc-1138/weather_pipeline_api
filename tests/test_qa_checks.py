import os
import psycopg2
import pytest

@pytest.mark.usefixtures("postgres_container")
def test_qa_checks():
    """
    Runs each QA SQL in sql/qa_checks.sql; fails if any check returns rows.
    """
    # Build connection parameters from env vars
    dsn = {
        "host":     os.environ["DB_HOST"],
        "port":     os.environ["DB_PORT"],
        "dbname":   os.environ["DB_NAME"],
        "user":     os.environ["DB_USER"],
        "password": os.environ["DB_PASSWORD"],
        "sslmode":  os.environ.get("DB_SSLMODE", "disable"),
    }

    # Connect and run each query in qa_checks.sql
    conn = psycopg2.connect(**dsn)
    cur = conn.cursor()

    # Split on semicolon + newline to get individual statements
    raw_sql = open("sql/qa_checks.sql").read().strip()
    queries = [q.strip() for q in raw_sql.split(";\n") if q.strip()]

    for query in queries:
        cur.execute(query)
        rows = cur.fetchall()
        assert not rows, f"QA check failed for:\n{query}\nReturned rows:\n{rows}"

    cur.close()
    conn.close()
