# Claude Code Prompt — EIA Oil Dashboard v1

## Project Overview

Build a full-stack oil market dashboard called **EIA Oil Dashboard** using:
- **Backend**: Python + FastAPI
- **Frontend**: React + Material UI (MUI Core, MIT licensed, free)
- **Local database**: DuckDB (file-based, no server required)
- **Data source**: EIA (US Energy Information Administration) API v2 only
- **Root folder**: `eia-oil-dashboard` (already exists as a cloned GitHub repo)

The goal is a clean, publicly shareable dashboard showing key US and global oil
market indicators. It must be fully reproducible — anyone cloning the repo should
be able to run it locally with just their own EIA API key in a `.env` file.

---

## Tech Stack Details

- Python 3.11+
- FastAPI + Uvicorn
- DuckDB (local file-based analytical database)
- pandas (data wrangling in ingestion scripts)
- requests (HTTP calls to EIA API)
- python-dotenv (loading `.env`)
- React 18 (Vite-based setup)
- Material UI (MUI Core v5, MIT licensed) for all UI components
- Recharts for line charts and bar charts
- React Simple Maps + D3 for the choropleth world map
- axios for frontend HTTP calls to FastAPI

---

## Project Structure

Create the following structure inside `eia-oil-dashboard/`:

```
eia-oil-dashboard/
├── backend/
│   ├── main.py               # FastAPI app, all API routes
│   ├── db.py                 # DuckDB connection and query helpers
│   ├── ingestion/
│   │   ├── fetch_eia.py      # All EIA API fetch functions
│   │   └── run_ingestion.py  # Manual trigger script — run this to refresh data
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── components/
│   │   │   ├── KpiCards.jsx
│   │   │   ├── CrudeStocksChart.jsx
│   │   │   ├── ProductionChart.jsx
│   │   │   ├── TopCountriesChart.jsx
│   │   │   └── WorldMap.jsx
│   │   └── api/
│   │       └── client.js     # axios base client pointing to FastAPI
│   ├── package.json
│   └── vite.config.js
├── data/
│   ├── bronze/               # Raw JSON/CSV from EIA API saved as Parquet
│   ├── silver/               # Cleaned and enriched Parquet files
│   └── oil_dashboard.duckdb  # DuckDB database file (gitignored)
├── .env.example              # Template showing required env vars (no real key)
├── .gitignore                # Must include .env and data/oil_dashboard.duckdb
└── README.md
```

---

## Environment Variables

The `.env` file (never committed) must contain:
```
EIA_API_KEY=your_key_here
```

The `.env.example` file (committed) must contain:
```
EIA_API_KEY=your_key_here
```

Load with `python-dotenv` in all Python scripts.

---

## Data Layer — DuckDB with Bronze/Silver/Gold Pattern

Use DuckDB as the local database stored at `data/oil_dashboard.duckdb`.

### Bronze layer (raw from EIA API)
Store raw API responses as-is. Tables:
- `bronze.us_weekly_stocks` — raw weekly US crude stocks data
- `bronze.us_monthly_production` — raw monthly US crude production
- `bronze.refinery_utilization` — raw weekly refinery utilization rate
- `bronze.international_production` — raw annual international production by country
- `bronze.crude_prices` — raw daily/weekly Brent and WTI spot prices

### Silver layer (cleaned)
Cleaned versions of bronze tables with:
- Proper date columns (parsed to DATE type)
- Nulls handled (EIA uses 0 or missing for unavailable data)
- Column names standardised to snake_case
- Units preserved as metadata columns

Tables mirror bronze: `silver.us_weekly_stocks`, `silver.us_monthly_production`,
`silver.refinery_utilization`, `silver.international_production`, `silver.crude_prices`

### Gold layer (aggregated for dashboard)
Pre-aggregated views for each dashboard panel:
- `gold.kpi_latest` — single-row view with all KPI values
- `gold.stocks_timeseries` — weekly stocks time series for line chart
- `gold.production_timeseries` — monthly US production for line chart
- `gold.top_countries` — top 15 countries by latest annual production for bar chart
- `gold.world_production_map` — country ISO codes + latest production value for choropleth

---

## EIA API Details

Base URL: `https://api.eia.gov/v2/`
API key passed as query parameter: `?api_key=YOUR_KEY`

**Important**: The API returns max 5,000 rows per request. Use `offset` parameter
for pagination when fetching long time series. Always paginate.

Reference the EIA API browser at `https://www.eia.gov/opendata/browser/` for
exploring endpoints.

### Endpoints to use

#### 1. US Weekly Crude Stocks
```
GET /petroleum/supply/weekly/wcrfpus2/data/
params: frequency=weekly, data[]=value, sort[0][column]=period, sort[0][direction]=desc
```
Unit: thousand barrels. Series covers US total commercial crude stocks.

#### 2. Cushing Oklahoma Stocks (overlay on stocks chart)
```
GET /petroleum/supply/weekly/wcrstus1/data/
params: frequency=weekly
```
Cushing is the WTI delivery point — traders watch this closely.

#### 3. US Monthly Crude Production
```
GET /petroleum/supply/monthly/prodtype/data/
params: frequency=monthly, facets[duoarea][]=NUS, facets[product][]=EPC0
```

#### 4. Weekly Refinery Utilization
```
GET /petroleum/operate/wref/data/
params: frequency=weekly, data[]=value
```
Returns refinery utilization as a percentage of operable capacity.

#### 5. International Production by Country (annual)
```
GET /international/data/
params: frequency=annual, data[]=value,
        facets[productId][]=55,   (crude oil incl. lease condensate)
        facets[activityId][]=1    (production)
```
This includes Russia, Saudi Arabia, US, all OPEC countries.

#### 6. WTI Spot Price
```
GET /petroleum/pri/spt/data/
params: frequency=daily, facets[series][]=RWTC
```

#### 7. Brent Spot Price
```
GET /petroleum/pri/spt/data/
params: frequency=daily, facets[series][]=RBRTE
```

---

## Ingestion Pipeline (`run_ingestion.py`)

This is a **manual trigger** script. The user runs it to refresh all data.
It should:
1. Call each fetch function in `fetch_eia.py`
2. Write raw responses to bronze DuckDB tables (upsert/replace)
3. Run bronze → silver transformations
4. Run silver → gold aggregations
5. Print clear progress messages so the user knows what is happening

The script must be runnable from the terminal:
```
cd backend
python ingestion/run_ingestion.py
```

---

## FastAPI Backend (`main.py`)

Create a FastAPI app with the following endpoints. All endpoints query DuckDB
gold tables and return JSON.

```
GET /api/kpi          → latest KPI values (prices, stocks, production, utilization)
GET /api/stocks       → weekly US crude stocks time series
GET /api/production   → monthly US crude production time series
GET /api/countries    → top countries by annual production
GET /api/world        → all countries with latest production for choropleth map
```

Enable CORS so the React frontend can call the backend during local development:
```python
allow_origins=["http://localhost:5173"]  # Vite default port
```

FastAPI should serve from `http://localhost:8000`.

---

## React Frontend

Use **Vite** to scaffold the React app inside `frontend/`.

### Styling
Use **Material UI (MUI Core v5)** for all layout and UI components.
Choose a **dark theme** — it looks professional for a data dashboard and works
well with charts and maps. Use MUI's `ThemeProvider` and `createTheme`.

The overall layout should be:
- A top `AppBar` with the dashboard title "EIA Oil Dashboard"
- A subtitle line: "Data source: U.S. Energy Information Administration"
- Main content in a responsive MUI `Grid` layout

### Dashboard Panels (v1)

#### 1. KPI Cards Row (`KpiCards.jsx`)
Four MUI `Card` components in a row (responsive: 2x2 on mobile, 4x1 on desktop):
- **Brent Price** — latest USD/barrel + change from previous day
- **WTI Price** — latest USD/barrel + change from previous day  
- **US Crude Stocks** — latest weekly figure in million barrels + WoW change
- **Refinery Utilization** — latest weekly % + WoW change

Each card shows: metric name, big bold number, unit, and a small coloured
trend indicator (green arrow up / red arrow down).

#### 2. US Crude Stocks Line Chart (`CrudeStocksChart.jsx`)
- Recharts `LineChart`
- Two lines: Total US stocks + Cushing Oklahoma stocks
- X axis: date, Y axis: thousand barrels
- Date range selector: 1Y / 3Y / 5Y / All
- Show a horizontal reference line for the 5-year average

#### 3. US Monthly Production Line Chart (`ProductionChart.jsx`)
- Recharts `LineChart`  
- Single line: US monthly crude production
- X axis: date, Y axis: thousand barrels/day
- Date range selector: 5Y / 10Y / All

#### 4. Top Countries Bar Chart (`TopCountriesChart.jsx`)
- Recharts `BarChart` (horizontal bars, easier to read country names)
- Top 15 countries by latest available annual production
- X axis: thousand barrels/day, Y axis: country name
- Highlight the US bar in a different colour

#### 5. World Choropleth Map (`WorldMap.jsx`)
- Use **React Simple Maps** + **D3-scale** for the choropleth
- Color scale: light yellow → dark orange/red for production intensity
- Tooltip on hover showing country name + production value
- Countries with no data shown in a neutral grey
- Use ISO 3166-1 alpha-3 country codes to join map geometry with EIA data
- Note: EIA international data uses its own country codes — handle the mapping
  to ISO codes in the gold layer transformation

---

## README.md

Write a clear README with:
1. Project description
2. Prerequisites (Python 3.11+, Node 18+, EIA API key)
3. Setup instructions:
   - Clone repo
   - Copy `.env.example` to `.env` and add EIA API key
   - `pip install -r backend/requirements.txt`
   - `cd backend && python ingestion/run_ingestion.py` (first data load)
   - `cd backend && uvicorn main:app --reload`
   - `cd frontend && npm install && npm run dev`
4. How to refresh data (run ingestion script manually)
5. Data source credit: U.S. Energy Information Administration

---

## .gitignore additions

Make sure these are in `.gitignore`:
```
.env
data/oil_dashboard.duckdb
data/bronze/
data/silver/
__pycache__/
*.pyc
node_modules/
frontend/dist/
```

The `data/gold/` folder does not need to be gitignored since gold layer lives
inside DuckDB, not as separate files.

---

## Coding Style Preferences

- Python: flat, linear scripts — no deep class hierarchies
- Functions must have docstrings explaining what they do and what they return
- Inline comments on non-obvious lines
- No global state in FastAPI — use dependency injection for DuckDB connection
- React components: functional components with hooks only
- Keep components focused — one responsibility per file

---

## Notes and Gotchas

- EIA API returns values as **strings** (standardised in v2.1.6) — always cast
  to float/int when writing to DuckDB
- Some EIA series use `null` for missing data, others use `0` — handle both
- The international production endpoint covers many energy types — always filter
  to `productId=55` (crude oil) and `activityId=1` (production)
- Recharts requires numeric X axis values or properly formatted date strings —
  parse dates carefully
- React Simple Maps needs TopoJSON world data — use the built-in world atlas
  or fetch from `https://cdn.jsdelivr.net/npm/world-atlas@2/countries-110m.json`
- EIA country codes do NOT match ISO codes directly — build a mapping dictionary
  in the gold transformation (the most common ones: USA=US, RUS=RS, SAU=SA, etc.)
  A complete mapping table will need to be hardcoded or looked up
