-- qa_checks.sql - Quality Assurance Queries for Weather Data

-- Check 1: Count of records with NULL temperature values.
SELECT COUNT(*) AS null_temperature_count
FROM weather_data
WHERE temperature IS NULL;

-- Check 2: Total number of records in the weather_data table.
SELECT COUNT(*) AS total_row_count
FROM weather_data;

-- Check 3: Count of records where precipitation exceeds 100 mm (as an example anomaly).
SELECT COUNT(*) AS high_precipitation_count
FROM weather_data
WHERE precipitation > 100;
