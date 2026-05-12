# EIA Oil Dashboard

A full-stack oil market dashboard showing key US and global crude oil indicators,
built with FastAPI, React, Material UI, and DuckDB. All data is sourced from the
U.S. Energy Information Administration (EIA) API v2.

## Dashboard panels

- **KPI cards** — latest Brent/WTI prices, US crude stocks, refinery utilization + day-over-day changes
- **US Crude Stocks** — weekly time series with Cushing Oklahoma overlay and 5-year average
- **US Monthly Production** — monthly crude output since 1983
- **Top Countries** — horizontal bar chart of the top 15 producing countries
- **World Choropleth** — production intensity map for all countries with EIA data

## Prerequisites

- Python 3.11+
- Node 18+
- A free EIA API key — register at https://www.eia.gov/opendata/register.php

## Setup

### 1. Clone and configure

```bash
git clone <repo-url>
cd eia-oil-dashboard
cp .env.example .env
# Edit .env and set your EIA_API_KEY
```

### 2. Install Python dependencies

Using a virtual environment is recommended to avoid conflicts:

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate

pip install -r backend/requirements.txt
```

### 3. Fetch initial data

This downloads all series from the EIA API and builds the local DuckDB database.
It takes a few minutes on first run.

```bash
cd backend
python ingestion/run_ingestion.py
```

### 4. Start the API server

```bash
cd backend
uvicorn main:app --reload
```

The API will be available at http://localhost:8000.

### 5. Start the frontend

In a separate terminal:

```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:5173 in your browser.

## Refreshing data

Run the ingestion script again at any time to pull the latest data from EIA:

```bash
cd backend
python ingestion/run_ingestion.py
```

## Tech stack

| Layer | Technology |
|-------|-----------|
| Backend API | Python 3.11 + FastAPI + Uvicorn |
| Database | DuckDB (file-based, no server needed) |
| Data fetch | requests + pandas |
| Frontend | React 18 + Vite |
| UI components | Material UI (MUI Core v5, MIT) |
| Charts | Recharts |
| Map | React Simple Maps + D3-scale |

## Data source

All data is provided by the **U.S. Energy Information Administration (EIA)**.
https://www.eia.gov/opendata/

The EIA API is free to use with a registered API key and is updated weekly/monthly
depending on the series.
