"""
test_api.py - Integration Tests for the FastAPI Application

This module uses FastAPI's TestClient to simulate HTTP requests to the API endpoints.
It helps verify that the /weather endpoint behaves as expected.
"""

from fastapi.testclient import TestClient
from app.main import app
import unittest

# Create a TestClient instance for testing the FastAPI app.
client = TestClient(app)

class TestAPI(unittest.TestCase):
    def test_get_weather_success(self):
        """
        Test the /weather endpoint with valid parameters.
        This test expects a 200 response and a JSON payload containing 'status' and 'rows_loaded'.
        """
        response = client.get("/weather", params={
            "venue_id": "test_venue",
            "start_date": "2024-01-01",
            "end_date": "2024-01-02"
        })
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("status", data)
        self.assertIn("rows_loaded", data)

    def test_get_weather_invalid_dates(self):
        """
        Test that an invalid date format results in a 422 error.
        FastAPI will return Unprocessable Entity for invalid date strings.
        """
        response = client.get("/weather", params={
            "venue_id": "test_venue",
            "start_date": "invalid-date",
            "end_date": "2024-01-02"
        })
        self.assertEqual(response.status_code, 422)

if __name__ == "__main__":
    unittest.main()
