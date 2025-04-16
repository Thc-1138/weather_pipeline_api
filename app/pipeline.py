"""
pipeline.py - ETL Pipeline for Weather Data

This module implements the full ETL process:
  1. Extraction: Retrieve historical weather data from the Open-Meteo API.
  2. Transformation: Convert the raw API data into a structured list of records.
  3. Loading: Insert the structured records into the PostgreSQL database.
  4. Orchestration: run_pipeline() ties these steps together.

Each record's keys are named to directly match the API's parameter names,
so our transformed data fields match what Open-Meteo returns.
"""

import requests
from app.db import get_db_connection

def extract_weather_data(lat, lon, start_date, end_date):
    """
    Extracts weather data from the Open-Meteo historical API.

    Args:
        lat (float): Latitude coordinate for the target location.
        lon (float): Longitude coordinate for the target location.
        start_date (str): Start date in 'YYYY-MM-DD' format.
        end_date (str): End date in 'YYYY-MM-DD' format.

    Returns:
        dict: The JSON response from the API.

    Note:
        The URL requests 15 specific hourly parameters to capture detailed weather data.
    """
    url = (
        f"https://archive-api.open-meteo.com/v1/archive?latitude={lat}"
        f"&longitude={lon}&start_date={start_date}&end_date={end_date}"
        # Requesting fields that will be used by the pipeline.
        "&hourly=temperature_2m,precipitation,snowfall,cloud_cover,wind_speed_10m,"
        "relative_humidity_2m,apparent_temperature,precipitation_probability,"
        "wind_gusts_10m,pressure_msl,wind_direction_10m,weather_code,rain,surface_pressure"
        "&timezone=UTC"
    )
    response = requests.get(url)
    response.raise_for_status()  # Throws HTTPError if the API request fails.
    return response.json()

def transform(data):
    """
    Transforms raw API data into a list of structured records.
    
    Expects 'hourly' data structured as a dictionary of lists (one list per field).
    Each record corresponds to a specific time, aligning indices across all fields.
    
    Args:
        data (dict): Raw JSON data returned by the API.
    
    Returns:
        list: A list of dictionaries. Each dictionary represents a weather record with keys that match the API names.
    
    Important:
        The output keys (e.g., 'temperature_2m', 'wind_direction_10m', 'weather_code', etc.)
        match the parameter names from the API for consistency.
    """
    hourly = data.get("hourly", {})
    timestamps = hourly.get("time", [])
    records = []
    # Loop over each timestamp index to construct individual records.
    for i, ts in enumerate(timestamps):
        record = {
            "timestamp": ts,
            "temperature_2m": hourly.get("temperature_2m", [None])[i],
            "precipitation": hourly.get("precipitation", [None])[i],
            "snowfall": hourly.get("snowfall", [None])[i],
            "cloud_cover": hourly.get("cloud_cover", [None])[i],
            "wind_speed_10m": hourly.get("wind_speed_10m", [None])[i],
            "relative_humidity_2m": hourly.get("relative_humidity_2m", [None])[i],
            "apparent_temperature": hourly.get("apparent_temperature", [None])[i],
            "precipitation_probability": hourly.get("precipitation_probability", [None])[i],
            "wind_gusts_10m": hourly.get("wind_gusts_10m", [None])[i],
            "pressure_msl": hourly.get("pressure_msl", [None])[i],
            "wind_direction_10m": hourly.get("wind_direction_10m", [None])[i],
            "weather_code": hourly.get("weather_code", [None])[i],
            "rain": hourly.get("rain", [None])[i],
            "surface_pressure": hourly.get("surface_pressure", [None])[i]
        }
        records.append(record)
    return records

def load(records, venue_id):
    """
    Loads the list of weather records into the PostgreSQL database.

    For each record in the provided list, this function executes an INSERT statement.
    
    Args:
        records (list): List of dictionaries representing weather records.
        venue_id (str): Identifier for the venue (e.g., a location code).
    
    Returns:
        int: The number of rows inserted into the database.
    
    Note:
        The INSERT query columns must match the keys produced by the transform() function.
    """
    conn = get_db_connection()  # Create a new database connection.
    cur = conn.cursor()
    insert_query = """
        INSERT INTO weather_data (
            venue_id, timestamp, temperature_2m, precipitation, snowfall, 
            cloud_cover, wind_speed_10m, relative_humidity_2m, apparent_temperature, 
            precipitation_probability, wind_gusts_10m, pressure_msl, wind_direction_10m, 
            weather_code, rain, surface_pressure
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    for rec in records:
        cur.execute(insert_query, (
            venue_id,
            rec["timestamp"],
            rec["temperature_2m"],
            rec["precipitation"],
            rec["snowfall"],
            rec["cloud_cover"],
            rec["wind_speed_10m"],
            rec["relative_humidity_2m"],
            rec["apparent_temperature"],
            rec["precipitation_probability"],
            rec["wind_gusts_10m"],
            rec["pressure_msl"],
            rec["wind_direction_10m"],
            rec["weather_code"],
            rec["rain"],
            rec["surface_pressure"]
        ))
    conn.commit()
    count = len(records)
    cur.close()
    conn.close()
    return count

def run_pipeline(venue_id, start_date, end_date):
    """
    Orchestrates the full ETL process.

    It extracts weather data (using hardcoded coordinates for demonstration),
    transforms the raw data into structured records, and loads them into the database.

    Args:
        venue_id (str): Identifier for the venue.
        start_date (str): Start date in 'YYYY-MM-DD' format.
        end_date (str): End date in 'YYYY-MM-DD' format.
    
    Returns:
        int: The total number of rows inserted into the database.
    """
    # Fixed coordinates are used here (representing, e.g., New York City).
    lat, lon = 40.71, -74.01  
    data = extract_weather_data(lat, lon, start_date, end_date)
    records = transform(data)
    inserted_count = load(records, venue_id)
    return inserted_count
