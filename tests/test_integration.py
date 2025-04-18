# File: tests/test_integration.py
"""
Integration Tests using Testcontainers for a real PostgreSQL database.
These tests spin up a Postgres Docker container, apply the schema,
then exercise the full /weather pipeline, verifying both API
response and database inserts.
"""
import os
import psycopg2
import pytest
import urllib.parse
from testcontainers.postgres import PostgresContainer
from fastapi.testclient import TestClient

# Fixture to start a Postgres container for the entire test session
@pytest.fixture(scope="session")
def postgres_container():
    """
    Starts a PostgreSQL container and sets connection info in environment variables.
    """
    with PostgresContainer("postgres:16-alpine") as postgres:
        # Parse the connection URL for host, port, database, user, and password
        conn_url = postgres.get_connection_url()
        parsed = urllib.parse.urlparse(conn_url)
        os.environ["DB_HOST"] = parsed.hostname
        os.environ["DB_PORT"] = str(parsed.port)
        os.environ["DB_NAME"] = parsed.path.lstrip('/')  # Remove leading '/'
        os.environ["DB_USER"] = parsed.username
        os.environ["DB_PASSWORD"] = parsed.password
        # Disable SSL for Testcontainers Postgres
        os.environ["DB_SSLMODE"] = "disable"

        # Initialize the database schema
        conn = psycopg2.connect(
            host=os.environ["DB_HOST"],
            port=os.environ["DB_PORT"],
            dbname=os.environ["DB_NAME"],
            user=os.environ["DB_USER"],
            password=os.environ["DB_PASSWORD"],
            sslmode=os.environ.get("DB_SSLMODE")
        )
        with conn.cursor() as cur:
            schema_sql = open("sql/schema.sql").read()
            cur.execute(schema_sql)
            conn.commit()
        conn.close()
        yield postgres

# Fixture to provide a TestClient configured to use the test DB
@pytest.fixture(scope="session")
def client(postgres_container):
    # Import here so that environment variables are set first
    from app.main import app
    return TestClient(app)

# Integration test verifying API and DB
def test_weather_pipeline_integration(client):
    # Call the endpoint
    response = client.get(
        "/weather",
        params={
            "venue_id": "integration_test",
            "start_date": "2024-01-01",
            "end_date": "2024-01-02"
        }
    )
    assert response.status_code == 200, f"Expected 200 but got {response.status_code}: {response.text}"
    data = response.json()
    assert data["status"] == "success"
    assert isinstance(data["rows_loaded"], int)

    # Verify that records were inserted into Postgres
    conn = psycopg2.connect(
        host=os.environ["DB_HOST"],
        port=os.environ["DB_PORT"],
        dbname=os.environ["DB_NAME"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        sslmode=os.environ.get("DB_SSLMODE")
    )
    with conn.cursor() as cur:
        cur.execute(
            "SELECT COUNT(*) FROM weather_data WHERE venue_id = %s",
            ("integration_test",)
        )
        count = cur.fetchone()[0]
    conn.close()
    assert count == data["rows_loaded"]
