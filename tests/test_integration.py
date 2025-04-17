# File: tests/test_integration.py
"""
Integration Tests using Testcontainers for a real PostgreSQL database.
These tests spin up a Postgres Docker container, apply the schema,
and then exercise the full /weather pipeline, verifying both API
response and database inserts.
"""
import os
import psycopg2
import pytest
from testcontainers.postgres import PostgresContainer
from fastapi.testclient import TestClient

# Fixture to start a Postgres container for the entire test session
@pytest.fixture(scope="session")
def postgres_container():
    with PostgresContainer("postgres:16-alpine") as postgres:
        # Expose connection info via environment variables
        os.environ["DB_HOST"] = postgres.get_container_host_ip()
        os.environ["DB_PORT"] = str(postgres.get_exposed_port(5432))
        os.environ["DB_NAME"] = postgres.DATABASE
        os.environ["DB_USER"] = postgres.USER
        os.environ["DB_PASSWORD"] = postgres.PASSWORD
        # Initialize schema
        conn = psycopg2.connect(
            host=os.environ["DB_HOST"],
            port=os.environ["DB_PORT"],
            dbname=os.environ["DB_NAME"],
            user=os.environ["DB_USER"],
            password=os.environ["DB_PASSWORD"],
            sslmode="disable"
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
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert isinstance(data["rows_loaded"], int)
    # Verify DB records
    conn = psycopg2.connect(
        host=os.environ["DB_HOST"],
        port=os.environ["DB_PORT"],
        dbname=os.environ["DB_NAME"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        sslmode="disable"
    )
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM weather_data WHERE venue_id = %s", ("integration_test",))
    count = cur.fetchone()[0]
    conn.close()
    assert count == data["rows_loaded"]