-- schema.sql - Database Schema for Weather Data
-- This script creates the 'weather_data' table with all required fields.
-- Each column has a comment explaining its purpose and unit of measure.

CREATE TABLE IF NOT EXISTS weather_data (
    id SERIAL PRIMARY KEY,                   -- Unique record identifier
    venue_id TEXT NOT NULL,                  -- Identifier for the data's venue or location
    timestamp TIMESTAMPTZ NOT NULL,          -- Timestamp of the weather data (with timezone)
    temperature_2m REAL,                        -- Temperature (°C)
    precipitation REAL,                      -- Total precipitation (mm)
    snowfall REAL,                           -- Snowfall (mm)
    cloud_cover INTEGER,                      -- Cloud cover percentage (0-100)
    wind_speed_10m REAL,                          -- Wind speed (m/s)
    relative_humidity_2m REAL,                  -- Relative humidity percentage (0-100)
    apparent_temperature REAL,               -- "Feels like" temperature (°C)
    precipitation_probability REAL,          -- Chance of precipitation (%) 
    wind_gusts_10m REAL,                     -- Wind gust speed (m/s)
    pressure_msl REAL,                       -- Atmospheric pressure at mean sea level (hPa)
    wind_direction_10m INTEGER,              -- Wind direction (degrees 0-360)
    weather_code INTEGER,                    -- Coded weather condition representation
    rain REAL,                               -- Rain amount (mm)
    surface_pressure REAL                    -- Surface atmospheric pressure (hPa)
);