"""
main.py - FastAPI Application Entry Point

This module creates a FastAPI application and defines an endpoint 
to trigger the ETL pipeline, which fetches, transforms, and loads
weather data into the PostgreSQL database.

Usage:
    Run with Uvicorn:
        uvicorn app.main:app --host=0.0.0.0 --port=8000 --reload

The interactive API documentation will be available at:
    http://127.0.0.1:8000/docs
"""

from fastapi import FastAPI, HTTPException
from datetime import date
from app.pipeline import run_pipeline

# Create an instance of the FastAPI app
app = FastAPI(title="Weather Pipeline API", version="1.0.0")

@app.get("/weather", summary="Trigger Weather Data Pipeline", 
         description="Fetches historical weather data and stores it in the database.")
def get_weather(venue_id: str, start_date: date, end_date: date):
    """
    Endpoint: GET /weather
    - venue_id: Unique identifier for the venue.
    - start_date: Start date for data (YYYY-MM-DD).
    - end_date: End date for data (YYYY-MM-DD).
    
    Returns:
        JSON response with the status and number of rows inserted into the database.
    """
    try:
        rows_loaded = run_pipeline(venue_id, start_date, end_date)
        return {"status": "success", "rows_loaded": rows_loaded}
    except Exception as e:
        # Return a 500 error if any exception occurs during pipeline execution.
        raise HTTPException(status_code=500, detail=str(e))
