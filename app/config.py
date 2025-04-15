"""
config.py - Centralized Configuration Module

This module loads configuration settings for the application using environment
variables. It uses python-dotenv to load variables from a .env file, which is used
for local development. In production, environment variables should be set via
the hosting platform.
"""

import os
from dotenv import load_dotenv

# Load environment variables from the .env file located in the project root.
load_dotenv()

# Database configuration variables
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "weather")
DB_USER = os.getenv("DB_USER", "weather_admin")
DB_PASSWORD = os.getenv("DB_PASSWORD", "Zr9!vB73xQm#LpN2")
DB_SSLMODE = os.getenv("DB_SSLMODE", "require")

# Additional configuration variables can be added here as needed.
