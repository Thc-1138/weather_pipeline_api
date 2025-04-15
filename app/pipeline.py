"""
pipeline.py - ETL Pipeline for Weather Data

This module defines the functions for the Extract-Transform-Load (ETL)
process:
  1. extract_weather_data: Retrieves weather data from Open-Meteo API.
  2. transform: Maps the API's response to a list of dictionaries that match the DB schema.
  3. load: Inserts the transformed data into the PostgreSQL table.
  4. run_pipeline: Orchestrates the ETL steps and returns the row count inserted.
"""

import requests
from app.db import get_db_connection

def extract_weather_data(lat, lon, start_date, end_date):
    """
    Extract weather data using the Open-Meteo historical API.
    
    Parameters:
        lat (float): Latitude for the location.
        lon (float): Longitude for the location.
        start_date (str): Date in 'YYYY-MM-DD' format for start.
        end_date (str): Date in 'YYYY-MM-DD' format for end.
        
    Returns:
        dict: JSON response from the API containing weather data.
    """
    url = (
        f"https://archive-api.open-meteo.com/v1/archive?latitude={lat}"
        f"&longitude={lon}&start_date={start_date}&end_date={end_date}"
        # Requesting 16 hourly parameters including the new fields
        "&hourly=temperature_2m,precipitation,snowfall,cloudcover,windspeed_10m,"
        "relative_humidity_2m,apparent_temperature,precipitation_probability,"
        "windgusts_10m,pressure_msl,wind_direction,weathercode,rain,surface_pressure"
        "&timezone=UTC"
    )
    response = requests.get(url)
    response.raise_for_status()  # Raises an error for unsuccessful API calls.
    return response.json()

def transform(data):
    """
    Transform the raw API response into a structured list of records.
    
    This function assumes the API returns an 'hourly' dictionary with lists for each field.
    Each record corresponds to a specific timestamp.
    
    Parameters:
        data (dict): The JSON data from the API.
        
    Returns:
        list: A list of dictionaries, each containing one row of weather data.
    """
    hourly = data.get("hourly", {})
    timestamps = hourly.get("time", [])
    rows = []
    for i, ts in enumerate(timestamps):
        row = {
            "timestamp": ts,
            "temperature": hourly.get("temperature_2m", [None])[i],
            "precipitation": hourly.get("precipitation", [None])[i],
            "snowfall": hourly.get("snowfall", [None])[i],
            "cloudcover": hourly.get("cloudcover", [None])[i],
            "windspeed": hourly.get("windspeed_10m", [None])[i],
            "relative_humidity": hourly.get("relative_humidity_2m", [None])[i],
            "apparent_temperature": hourly.get("apparent_temperature", [None])[i],
            "precipitation_probability": hourly.get("precipitation_probability", [None])[i],
            "windgusts": hourly.get("windgusts_10m", [None])[i],
            "pressure_msl": hourly.get("pressure_msl", [None])[i],
            "wind_direction": hourly.get("wind_direction", [None])[i],
            "weathercode": hourly.get("weathercode", [None])[i],
            "rain": hourly.get("rain", [None])[i],
            "surface_pressure": hourly.get("surface_pressure", [None])[i]
        }
        rows.append(row)
    return rows

def load(rows, venue_id):
    """
    Load the transformed weather records into the PostgreSQL database.
    
    Parameters:
        rows (list): The list of records to load.
        venue_id (str): An identifier for the venue.
        
    Returns:
        int: The number of rows successfully inserted.
    """
    conn = get_db_connection()
    cur = conn.cursor()
    insert_query = """
        INSERT INTO weather_data (
            venue_id, timestamp, temperature, precipitation, snowfall, 
            cloudcover, windspeed, relative_humidity, apparent_temperature, 
            precipitation_probability, windgusts, pressure_msl, wind_direction, 
            weathercode, rain, surface_pressure
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    for row in rows:
        cur.execute(insert_query, (
            venue_id,
            row["timestamp"],
            row["temperature"],
            row["precipitation"],
            row["snowfall"],
            row["cloudcover"],
            row["windspeed"],
            row["relative_humidity"],
            row["apparent_temperature"],
            row["precipitation_probability"],
            row["windgusts"],
            row["pressure_msl"],
            row["wind_direction"],
            row["weathercode"],
            row["rain"],
            row["surface_pressure"]
        ))
    conn.commit()
    inserted_count = len(rows)
    cur.close()
    conn.close()
    return inserted_count

def run_pipeline(venue_id, start_date, end_date):
    """
    Run the full ETL pipeline: extract weather data, transform it, and load into the database.
    
    For demonstration, fixed coordinates (e.g., New York City) are used.
    In production, map the venue_id to geographic coordinates.
    
    Parameters:
        venue_id (str): Identifier for the venue.
        start_date (str): Start date in 'YYYY-MM-DD' format.
        end_date (str): End date in 'YYYY-MM-DD' format.
        
    Returns:
        int: The number of rows inserted into the database.
    """
    # Example coordinates for New York City
    lat, lon = 40.71, -74.01  
    data = extract_weather_data(lat, lon, start_date, end_date)
    rows = transform(data)
    count = load(rows, venue_id)
    return count
