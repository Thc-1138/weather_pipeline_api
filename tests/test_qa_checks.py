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
# Read DB connection settings now that the postgres_container fixture has run
dsn = {
    'host': os.environ.get('DB_HOST'),
    'port': os.environ.get('DB_PORT'),
    'dbname': os.environ.get('DB_NAME'),
    'user': os.environ.get('DB_USER'),
    'password': os.environ.get('DB_PASSWORD'),
    'sslmode': os.environ.get('DB_SSLMODE', 'disable'),
}
# Ensure environment variables are present
missing = [k for k, v in dsn.items() if v is None]
assert not missing, f"Missing environment variables for DB connection: {missing}"

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