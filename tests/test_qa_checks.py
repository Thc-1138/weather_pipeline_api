"""
Integration test to run QA checks SQL queries against the test database.
Any non-empty result indicates a data inconsistency.
"""
import os
import psycopg2
import pytest

@pytest.mark.usefixtures("postgres_container")
def test_qa_checks():
    """
    Execute each QA check in sql/qa_checks.sql; fail if any check returns rows.
    """
dsn = dict(
    host=os.environ["DB_HOST"],
    port=os.environ["DB_PORT"],
    dbname=os.environ["DB_NAME"],
    user=os.environ["DB_USER"],
    password=os.environ["DB_PASSWORD"],
    sslmode=os.environ.get("DB_SSLMODE", "disable")
)
conn = psycopg2.connect(**dsn)
cur = conn.cursor()

# Load and split queries
sql = open("sql/qa_checks.sql").read().strip()
queries = [q.strip() for q in sql.split(";\n") if q.strip()]

for query in queries:
    cur.execute(query)
    rows = cur.fetchall()
    assert not rows, f"QA check failed for query:\n{query}\nViolations: {rows}"

cur.close()
conn.close()