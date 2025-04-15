-- SQL script to create your DB schema

CREATE TABLE IF NOT EXISTS weather_data (
    id SERIAL PRIMARY KEY,
    venue_id TEXT NOT NULL,
    timestamp TIMESTAMPTZ NOT NULL,
    temperature REAL,
    precipitation REAL,
    snowfall REAL,
    cloudcover INTEGER,
    windspeed REAL
);
