-- qa_checks.sql - Quality Assurance Queries for Weather Data


-- 1. No NULLs in critical columns
-- Returns rows where any required field is NULL
SELECT id, venue_id, timestamp
FROM weather_data
WHERE venue_id IS NULL
OR timestamp IS NULL
OR temperature IS NULL
OR precipitation IS NULL;

-- 2. Unique (venue_id, timestamp)
-- Returns duplicates of (venue_id, timestamp)
SELECT venue_id, timestamp, COUNT() AS cnt
FROM weather_data
GROUP BY venue_id, timestamp
HAVING COUNT() > 1;

-- 3. Value ranges
-- Temperature should be between -100 and 60 Celsius
SELECT id, temperature
FROM weather_data
WHERE temperature < -100 OR temperature > 60;

-- Precipitation >= 0
SELECT id, precipitation
FROM weather_data
WHERE precipitation < 0;

-- Snowfall >= 0
SELECT id, snowfall
FROM weather_data
WHERE snowfall < 0;

-- 4. Valid weather codes (0-99)
SELECT id, weather_code
FROM weather_data
WHERE weather_code < 0 OR weather_code > 99;