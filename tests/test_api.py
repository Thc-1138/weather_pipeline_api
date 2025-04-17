# weather_pipeline_api/tests/test_api.py

"""
test_api.py - Integration Tests for FastAPI Endpoints with Dependency Override

This module uses FastAPI's TestClient and overrides the get_pipeline_runner
dependency so that tests do not require a real database or external API.
"""

import unittest
from fastapi.testclient import TestClient
from app.main import app, get_pipeline_runner

# Override the pipeline runner dependency to return a fixed row count
app.dependency_overrides[get_pipeline_runner] = lambda: (lambda venue_id, start_date, end_date: 1)

client = TestClient(app)

class TestAPI(unittest.TestCase):
    def test_get_weather_success(self):
        """
        Verify that /weather returns status 200 and the stubbed rows_loaded value.
        """
        response = client.get(
            "/weather",
            params={
                "venue_id": "test_venue",
                "start_date": "2024-01-01",
                "end_date": "2024-01-02"
            }
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "success")
        self.assertEqual(data["rows_loaded"], 1)

    def test_get_weather_invalid_dates(self):
        """
        Ensure invalid date formats return a 422 error.
        """
        response = client.get(
            "/weather",
            params={
                "venue_id": "test_venue",
                "start_date": "invalid-date",
                "end_date": "2024-01-02"
            }
        )
        self.assertEqual(response.status_code, 422)

if __name__ == "__main__":
    unittest.main()