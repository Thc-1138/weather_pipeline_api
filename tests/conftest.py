# tests/conftest.py

import os
import psycopg2
import urllib.parse
import pytest
from testcontainers.postgres import PostgresContainer

@pytest.fixture(scope="session")
def postgres_container():
    """
    Starts a PostgreSQL container and sets connection info in environment variables.
    """
    with PostgresContainer("postgres:16-alpine") as postgres:
        conn_url = postgres.get_connection_url()
        parsed = urllib.parse.urlparse(conn_url)
        os.environ["DB_HOST"]     = parsed.hostname
        os.environ["DB_PORT"]     = str(parsed.port)
        os.environ["DB_NAME"]     = parsed.path.lstrip('/')
        os.environ["DB_USER"]     = parsed.username
        os.environ["DB_PASSWORD"] = parsed.password
        os.environ["DB_SSLMODE"]  = "disable"

        # Initialize your schema
        conn = psycopg2.connect(
            host=os.environ["DB_HOST"],
            port=os.environ["DB_PORT"],
            dbname=os.environ["DB_NAME"],
            user=os.environ["DB_USER"],
            password=os.environ["DB_PASSWORD"],
            sslmode=os.environ.get("DB_SSLMODE")
        )
        with conn.cursor() as cur:
            cur.execute(open("sql/schema.sql").read())
            conn.commit()
        conn.close()

        yield postgres
