"""
main.py - FastAPI Application Entry Point with Dependency Injection

This module sets up a FastAPI application and defines a GET endpoint that
triggers the ETL pipeline. The pipeline runner is provided via a FastAPI
dependency (get_pipeline_runner), making it easy to override in tests.
"""

from fastapi import FastAPI, HTTPException, Depends
from datetime import date
from app.pipeline import run_pipeline as default_run_pipeline

app = FastAPI(title="Weather Pipeline API", version="1.0.0")

def get_pipeline_runner():
    """
    Dependency that returns the pipeline runner function.
    Override this in tests via app.dependency_overrides.
    """
    return default_run_pipeline

@app.get(
    "/weather",
    summary="Trigger Weather Data Pipeline",
    description="Fetches historical weather data and stores it in the database."
)
def get_weather(
    venue_id: str,
    start_date: date,
    end_date: date,
    run_pipeline=Depends(get_pipeline_runner)
):
    """
    Endpoint: GET /weather
    - venue_id: Unique identifier for the venue.
    - start_date: Start date for data (YYYY-MM-DD).
    - end_date: End date for data (YYYY-MM-DD).

    Returns:
        JSON response with 'status' and 'rows_loaded'.
        Raises HTTPException(500) on errors.
    """
    try:
        rows_loaded = run_pipeline(venue_id, start_date, end_date)
        return {"status": "success", "rows_loaded": rows_loaded}
    except Exception as e:
        # Propagate exceptions as HTTP 500 for visibility
        raise HTTPException(status_code=500, detail=str(e))