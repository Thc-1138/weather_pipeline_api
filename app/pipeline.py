# ETL logic: extract, transform, load

import requests
from app.db import get_db_connection

def extract_weather_data(lat, lon, start_date, end_date):
    url = (f"https://archive-api.open-meteo.com/v1/archive?latitude={lat}&longitude={lon}"
           f"&start_date={start_date}&end_date={end_date}"
           "&hourly=temperature_2m,precipitation,snowfall,cloudcover,windspeed_10m&timezone=UTC")
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def transform(data):
    hourly = data.get('hourly', {})
    timestamps = hourly.get('time', [])
    rows = []
    for i, ts in enumerate(timestamps):
        row = {
            'timestamp': ts,
            'temperature': hourly.get('temperature_2m', [None])[i],
            'precipitation': hourly.get('precipitation', [None])[i],
            'snowfall': hourly.get('snowfall', [None])[i],
            'cloudcover': hourly.get('cloudcover', [None])[i],
            'windspeed': hourly.get('windspeed_10m', [None])[i]
        }
        rows.append(row)
    return rows

def load(rows, venue_id):
    conn = get_db_connection()
    cur = conn.cursor()
    insert_query = '''
        INSERT INTO weather_data (venue_id, timestamp, temperature, precipitation, snowfall, cloudcover, windspeed)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    '''
    for row in rows:
        cur.execute(insert_query, (
            venue_id,
            row['timestamp'],
            row['temperature'],
            row['precipitation'],
            row['snowfall'],
            row['cloudcover'],
            row['windspeed']
        ))
    conn.commit()
    count = len(rows)
    cur.close()
    conn.close()
    return count

def run_pipeline(venue_id, start_date, end_date):
    # Example: Use fixed coordinates (e.g., NYC); in production, map venue_id to coordinates
    lat, lon = 40.71, -74.01
    data = extract_weather_data(lat, lon, start_date, end_date)
    rows = transform(data)
    return load(rows, venue_id)
