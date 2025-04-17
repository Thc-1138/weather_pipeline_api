# Weather Pipeline API

This project is a Python-based ETL pipeline and API that fetches historical weather data, transforms it, and loads it into a PostgreSQL database hosted on Azure.

## Overview

The ETL process includes:

- **Extract:** Retrieve historical weather data from the Open-Meteo API.  
- **Transform:** Process the JSON response into a format matching our database schema.  
- **Load:** Insert the transformed data into the `weather_data` table.

The API is built with **FastAPI** and exposes an endpoint to trigger the ETL process.

## Project Structure

<pre>
weather_pipeline_api/
├── app/               # Application source code
│   ├── __init__.py    # Initializes the app package
│   ├── main.py        # FastAPI entry point
│   ├── pipeline.py    # ETL pipeline logic
│   ├── db.py          # Database connection logic
│   ├── models.py      # (Optional) ORM models or constants
│   └── config.py      # Loads configuration from environment variables
├── sql/               # SQL scripts to create the schema and run QA checks
│   ├── schema.sql
│   └── qa_checks.sql
├── tests/             # Unit and integration tests
│   ├── __init__.py
│   ├── test_pipeline.py
│   └── test_api.py
├── .env               # Environment variables (for local development)
├── .gitignore         # Git ignore settings
├── requirements.txt   # Python dependency list
├── README.md          # Project documentation (this file)
├── Dockerfile         # (Optional) Docker configuration for containerization
├── azure-pipelines.yml  # (Optional) Azure DevOps CI/CD configuration
└── .github/
    └── workflows/
        └── deploy.yml   # (Optional) GitHub Actions workflow for deployment
</pre>

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/Thc-1138/weather_pipeline_api.git
cd weather_pipeline_api
```

### 2. Set Up the Virtual Environment

```bash
python -m venv venv
```

Activate the environment:

- **Windows (CMD):**
  ```bash
  venv\Scripts\activate
  ```
- **Windows (PowerShell):**
  ```powershell
  .\venv\Scripts\Activate.ps1
  ```
- **macOS/Linux:**
  ```bash
  source venv/bin/activate
  ```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a file named `.env` in the project root:

```dotenv
DB_HOST=weather-db-thc.postgres.database.azure.com
DB_PORT=5432
DB_NAME=weather
DB_USER=weather_admin
DB_PASSWORD=Zr9!vB73xQm#LpN2
DB_SSLMODE=require
```

### 5. Set Up the Database Schema

Run the SQL script from `sql/schema.sql` on your PostgreSQL database to create the necessary table.

### 6. Run the Application Locally

Start the FastAPI app using Uvicorn:

```bash
uvicorn app.main:app --reload
```

Visit [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) to view the interactive API documentation (Swagger UI).

### 7. Run Tests

Execute all unit and integration tests:

```bash
python -m unittest discover tests
```

## Deployment

- **Docker:** The provided `Dockerfile` can be used to containerize the application.  
- **CI/CD Pipelines:**
  - `azure-pipelines.yml` for Azure DevOps  
  - `.github/workflows/ci-cd.yml` for GitHub Actions

These pipelines automate testing and deployment when changes are pushed to the `master` branch.

## License

This project is licensed under the MIT License.
