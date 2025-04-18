-- sql/qa_checks.sql

-- 1) No NULLs in key columns
SELECT *
  FROM weather_data
 WHERE venue_id IS NULL
    OR timestamp    IS NULL;

-- 2) No duplicate (venue_id, timestamp) rows
SELECT venue_id,
       timestamp,
       COUNT(*) AS cnt
  FROM weather_data
 GROUP BY venue_id, timestamp
HAVING COUNT(*) > 1;

-- 3) Reasonable ranges for numeric fields
-- (adjust thresholds to your expected units if needed)

-- Temperature (°C)
SELECT *
  FROM weather_data
 WHERE temperature_2m < -50
    OR temperature_2m > 60;

-- Precipitation (mm)
SELECT *
  FROM weather_data
 WHERE precipitation < 0;

-- Snowfall (cm)
SELECT *
  FROM weather_data
 WHERE snowfall < 0;

-- Cloud cover (%)
SELECT *
  FROM weather_data
 WHERE cloud_cover < 0
    OR cloud_cover > 100;

-- Wind speed (m/s)
SELECT *
  FROM weather_data
 WHERE wind_speed_10m < 0;

-- Relative humidity (%)
SELECT *
  FROM weather_data
 WHERE relative_humidity_2m < 0
    OR relative_humidity_2m > 100;

-- Apparent temperature (°C)
SELECT *
  FROM weather_data
 WHERE apparent_temperature < -80
    OR apparent_temperature > 70;

-- Precipitation probability (%)
SELECT *
  FROM weather_data
 WHERE precipitation_probability < 0
    OR precipitation_probability > 100;

-- Wind gusts (m/s)
SELECT *
  FROM weather_data
 WHERE wind_gusts_10m < 0;

-- Mean sea–level pressure (hPa)
SELECT *
  FROM weather_data
 WHERE pressure_msl < 800
    OR pressure_msl > 1100;

-- Wind direction (°)
SELECT *
  FROM weather_data
 WHERE wind_direction_10m < 0
    OR wind_direction_10m > 360;

-- Weather code (API code values, non‑negative)
SELECT *
  FROM weather_data
 WHERE weather_code < 0;

-- Rain (mm)
SELECT *
  FROM weather_data
 WHERE rain < 0;

-- Surface pressure (hPa)
SELECT *
  FROM weather_data
 WHERE surface_pressure < 800
    OR surface_pressure > 1100;
