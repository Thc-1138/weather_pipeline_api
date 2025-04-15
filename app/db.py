"""
db.py - Database Connection Module

This module is responsible for creating and returning a connection to the
PostgreSQL database using psycopg2. The connection parameters are loaded
from environment variables for security and portability.
"""

import os
import psycopg2
from dotenv import load_dotenv

# Load environment variables from the .env file in the project root.
load_dotenv()

def get_db_connection():
    """
    Establish a connection to the PostgreSQL database.

    Connection parameters are retrieved from environment variables:
      - DB_HOST: The PostgreSQL server host.
      - DB_PORT: Port number, typically 5432.
      - DB_NAME: The name of the database to connect to.
      - DB_USER: Database username.
      - DB_PASSWORD: Database password.
      - DB_SSLMODE: SSL mode for secure connection (default: require).

    Returns:
        psycopg2.extensions.connection: A new database connection.
    """
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        sslmode=os.getenv("DB_SSLMODE", "require")
    )
    return conn
