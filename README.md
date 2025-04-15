# Weather Pipeline API

This project is a Python-based ETL data pipeline and API for fetching historical weather data and storing it in an Azure PostgreSQL database.

## Overview

- **Extract:** Retrieve historical weather data from the Open-Meteo API.
- **Transform:** Process the JSON response into a format that matches our database schema.
- **Load:** Insert the transformed data into the `weather_data` table.

The API is built with FastAPI and provides an endpoint to trigger the ETL process.

## Project Structure

