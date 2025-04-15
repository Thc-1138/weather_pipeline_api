-- schema.sql - Database Schema for Weather Data
-- This script creates the 'weather_data' table with all required fields.
-- Each column has a comment explaining its purpose and unit of measure.

CREATE TABLE IF NOT EXISTS weather_data (
    id SERIAL PRIMARY KEY,                   -- Unique record identifier
    venue_id TEXT NOT NULL,                  -- Identifier for the data's venue or location
    timestamp TIMESTAMPTZ NOT NULL,          -- Timestamp of the weather data (with timezone)
    temperature REAL,                        -- Temperature (°C)
    precipitation REAL,                      -- Total precipitation (mm)
    snowfall REAL,                           -- Snowfall (mm)
    cloudcover INTEGER,                      -- Cloud cover percentage (0-100)
    windspeed REAL,                          -- Wind speed (m/s)
    relative_humidity REAL,                  -- Relative humidity percentage (0-100)
    apparent_temperature REAL,               -- "Feels like" temperature (°C)
    precipitation_probability REAL,          -- Chance of precipitation (%) 
    windgusts REAL,                          -- Wind gust speed (m/s)
    pressure_msl REAL,                       -- Atmospheric pressure at mean sea level (hPa)
    wind_direction INTEGER,                  -- Wind direction (degrees 0-360)
    weathercode INTEGER,                     -- Coded weather condition representation
    rain REAL,                               -- Rain amount (mm)
    surface_pressure REAL                    -- Surface atmospheric pressure (hPa)
);
