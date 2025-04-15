"""
test_pipeline.py - Unit Tests for the ETL Pipeline

This module contains tests for the transform function in the ETL pipeline.
It verifies that data is correctly processed from the API response format
to the list of dictionaries that match the database schema.
"""

import unittest
from app.pipeline import transform

class TestPipeline(unittest.TestCase):
    def test_transform_empty_data(self):
        """
        Test that an empty 'hourly' response returns an empty list.
        """
        data = {"hourly": {"time": [], "temperature_2m": []}}
        result = transform(data)
        self.assertEqual(result, [])

    def test_transform_valid_data(self):
        """
        Test that the transform function correctly aligns the hourly values.
        """
        data = {
            "hourly": {
                "time": ["2024-01-01T00:00:00Z", "2024-01-01T01:00:00Z"],
                "temperature_2m": [5.0, 6.0],
                "precipitation": [0.0, 0.1],
                "snowfall": [0.0, 0.0],
                "cloudcover": [80, 85],
                "windspeed_10m": [3.5, 4.0],
                "relative_humidity_2m": [60, 65],
                "apparent_temperature": [4.5, 5.5],
                "precipitation_probability": [20, 25],
                "windgusts_10m": [5.0, 5.5],
                "pressure_msl": [1012, 1011],
                "wind_direction": [180, 190],
                "weathercode": [0, 1],
                "rain": [0.0, 0.05],
                "surface_pressure": [1010, 1009]
            }
        }
        result = transform(data)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["temperature"], 5.0)
        self.assertEqual(result[1]["wind_direction"], 190)

if __name__ == "__main__":
    unittest.main()
