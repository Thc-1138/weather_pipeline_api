-- SQL queries for data quality/consistency

-- Example: Check for null temperature values
SELECT COUNT(*) FROM weather_data WHERE temperature IS NULL;
