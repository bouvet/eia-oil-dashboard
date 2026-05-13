# Claude Code Prompt v2 — EIA Oil Dashboard (Clean Rebuild)

## Important instructions before you start

1. **Check package versions first**: Before writing `pyproject.toml` or
   `package.json`, look up the current stable versions of ALL dependencies
   online. Never assume versions from training data. Verify that all packages
   are mutually compatible before writing the files.

2. **Check Node.js engine requirements**: Make sure the versions of Vite and
   other build tools you choose are compatible with Node.js LTS (22.x).

3. **A verified `fetch_eia.py` is already provided at the root of the repo**.
   Do not rewrite or modify it. Just move it to `backend/ingestion/fetch_eia.py`.
   All EIA endpoints and series codes in it are verified and working.

4. **Read this entire prompt before writing any code.**

---

## Project Overview

Build a full-stack oil market dashboard called **EIA Oil Dashboard** using:
- **Backend**: Python + FastAPI
- **Frontend**: React + Material UI (MUI Core, MIT licensed, free)
- **Local database**: DuckDB (file-based, no server required)
- **Data source**: EIA (US Energy Information Administration) API v2 only
- **Root folder**: `eia-oil-dashboard` (already exists as a cloned GitHub repo)

The goal is a clean, publicly shareable dashboard showing key US and global
oil market indicators. It must be fully reproducible — anyone cloning the repo
should be able to run it locally with just their own EIA API key in a `.env`
file.

---

## Tech Stack

- Python 3.11+
- **uv** for Python package and virtual environment management (replaces pip/venv)
- FastAPI + Uvicorn
- DuckDB (local file-based analytical database)
- pandas (data wrangling in ingestion scripts)
- requests (HTTP calls to EIA API — already used in fetch_eia.py)
- python-dotenv (loading .env)
- React 18 (Vite-based setup) — **pin to React 18.x, not 19**, because
  react-simple-maps does not yet support React 19
- Material UI (MUI Core, MIT licensed) for all UI components
- Recharts for line charts and bar charts
- React Simple Maps + D3 for the choropleth world map
- axios for frontend HTTP calls to FastAPI

---

## Project Structure

Create the following structure inside `eia-oil-dashboard/`:

```
eia-oil-dashboard/
├── backend/
│   ├── main.py                  # FastAPI app, all API routes
│   ├── db.py                    # DuckDB connection — single shared connection
│   ├── ingestion/
│   │   ├── fetch_eia.py         # Move from repo root — do not modify
│   │   └── run_ingestion.py     # Manual trigger script
│   └── pyproject.toml           # uv project file (replaces requirements.txt)
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
│   │       └── client.js        # axios base client pointing to FastAPI
│   ├── package.json
│   └── vite.config.js
├── data/
│   └── oil_dashboard.duckdb     # DuckDB database file (gitignored)
├── .env.example
├── .gitignore
└── README.md
```

---

## Python Environment — uv

Use **uv** for all Python package and environment management. Do not use pip
or venv directly.

The backend must be set up as a uv project with a `pyproject.toml` at
`backend/pyproject.toml`. This replaces `requirements.txt`.

Key uv commands for the README:
```
# Create virtual environment and install all dependencies
cd backend
uv sync

# Run the ingestion script
uv run python ingestion/run_ingestion.py

# Start the FastAPI server
uv run uvicorn main:app --reload
```

The `pyproject.toml` must declare all dependencies with pinned versions
(looked up online before writing). Use the `[project]` and
`[tool.uv]` sections. uv will generate a `uv.lock` file automatically —
commit this file to the repo so installs are fully reproducible.

Add to `.gitignore`:
```
.venv/
```
The `.venv/` folder is created by uv inside `backend/` — do not commit it.



`.env` file (never committed):
```
EIA_API_KEY=your_key_here
```

`.env.example` file (committed):
```
EIA_API_KEY=your_key_here
```

---

## Data Layer — DuckDB with Bronze/Silver/Gold Pattern

Use DuckDB stored at `data/oil_dashboard.duckdb`.

### Bronze layer (raw from EIA API)
- `bronze.us_weekly_stocks`
- `bronze.cushing_stocks`
- `bronze.us_monthly_production`
- `bronze.refinery_utilization`
- `bronze.international_production`
- `bronze.crude_prices`

### Silver layer (cleaned)
Same table names under `silver` schema, with:
- Proper DATE columns parsed from EIA period strings
- Nulls handled (EIA uses 0 or missing for unavailable data)
- Column names in snake_case
- Units preserved as metadata columns

### Gold layer (pre-aggregated for dashboard)
- `gold.kpi_latest` — view with all KPI values in a single row
- `gold.stocks_timeseries` — weekly stocks + Cushing joined by date
- `gold.production_timeseries` — monthly US production
- `gold.top_countries` — top 15 countries by latest annual production
- `gold.world_production_map` — all countries with latest production for map

---

## EIA API — Verified Endpoints and Series Codes

The `fetch_eia.py` file already implements all of these correctly.
This section is for reference only — do not reimplement fetch logic.

Base URL: `https://api.eia.gov/v2/`
Max rows per request: 5,000 — pagination with `offset` is already handled
in `fetch_eia.py`.

| Series | Endpoint | Series code | Unit |
|---|---|---|---|
| US weekly crude stocks | `petroleum/stoc/wstk/data/` | `WCESTUS1` | thousand barrels |
| Cushing OK stocks | `petroleum/stoc/wstk/data/` | `W_EPC0_SAX_YCUOK_MBBL` | thousand barrels |
| US monthly production | `petroleum/crd/crpdn/data/` | `MCRFPUS2` | thousand barrels/day |
| Refinery utilization | `petroleum/pnp/wiup/data/` | `WPULEUS3` | % of operable capacity |
| International production | `international/data/` | productId=55, activityId=1 | thousand barrels/day |
| WTI spot price | `petroleum/pri/spt/data/` | `RWTC` | USD/barrel |
| Brent spot price | `petroleum/pri/spt/data/` | `RBRTE` | USD/barrel |

---

## Backend — FastAPI (`main.py`)

### Database connection — IMPORTANT
Use a **single shared DuckDB connection** created at app startup, not a new
connection per request. Opening a new DuckDB connection on every API call is
inefficient and risks file locking issues under concurrent requests.

Implement it like this:
```python
# Single connection created at startup
_conn = None

def get_db():
    global _conn
    if _conn is None:
        _conn = get_connection()
    return _conn
```

Enable CORS for local development:
```python
allow_origins=["http://localhost:5173"]
allow_methods=["GET"]
```

### API endpoints
```
GET /api/kpi          → single-row KPI object
GET /api/stocks       → weekly stocks time series
GET /api/production   → monthly production time series
GET /api/countries    → top 15 countries by production
GET /api/world        → all countries for choropleth map
```

All endpoints query DuckDB gold layer and return JSON.
Handle NaN and pandas Timestamps carefully — convert to None and ISO date
strings before returning.

---

## Ingestion Pipeline (`run_ingestion.py`)

Manual trigger script. Run from terminal:
```
cd backend
python ingestion/run_ingestion.py
```

Steps:
1. Fetch all series using functions from `fetch_eia.py`
2. Write raw data to bronze DuckDB tables (full replace each run)
3. Transform bronze → silver
4. Build gold views from silver
5. Print clear progress messages at each step

### Silver transformations — important details

**Stocks and prices**: EIA period format is `YYYY-MM-DD` — cast directly to DATE.

**Monthly production**: EIA period format is `YYYY-MM` — append `-01` before
casting to DATE: `CAST(period || '-01' AS DATE)`.

**International production**: EIA returns country codes in `countryRegionId`.
These are mostly ISO 3166-1 alpha-3 already, but a small number differ.
Use the `EIA_TO_ISO3` mapping dictionary from the previous version of
`run_ingestion.py` (reproduced below) to handle overrides via a temp table join.

**Filtering aggregates**: In the gold layer, exclude regional/world aggregates
from the international production data using:
```sql
WHERE LENGTH(eia_country_code) = 3
  AND eia_country_code NOT IN (
    'OPE','OEC','WOR','NON','NAM','CAM','SAM','EUR','MEA','AFR','ASI','OCN'
  )
```

### EIA_TO_ISO3 mapping dictionary
Use this exact dictionary in `run_ingestion.py`:

```python
EIA_TO_ISO3 = {
    "USA": "USA", "RUS": "RUS", "SAU": "SAU", "CAN": "CAN", "IRQ": "IRQ",
    "CHN": "CHN", "IRN": "IRN", "ARE": "ARE", "UAE": "ARE", "BRA": "BRA",
    "KWT": "KWT", "MEX": "MEX", "KAZ": "KAZ", "NGA": "NGA", "NOR": "NOR",
    "LBY": "LBY", "ALG": "DZA", "AGO": "AGO", "ANG": "AGO", "VEN": "VEN",
    "OMN": "OMN", "GBR": "GBR", "COL": "COL", "AZE": "AZE", "IDN": "IDN",
    "IND": "IND", "MYS": "MYS", "ECU": "ECU", "ARG": "ARG", "QAT": "QAT",
    "GAB": "GAB", "COG": "COG", "EQG": "GNQ", "GNQ": "GNQ", "TTO": "TTO",
    "SSD": "SSD", "YEM": "YEM", "BRN": "BRN", "SYR": "SYR", "SDN": "SDN",
    "MRT": "MRT", "TCD": "TCD", "GHA": "GHA", "TZA": "TZA", "CMR": "CMR",
    "CIV": "CIV", "MOZ": "MOZ", "PER": "PER", "CHL": "CHL", "BOL": "BOL",
    "AUS": "AUS", "BHR": "BHR", "DEN": "DNK", "DNK": "DNK", "ITA": "ITA",
    "EGY": "EGY", "ROM": "ROU", "CZE": "CZE", "HUN": "HUN", "POL": "POL",
    "UKR": "UKR", "TKM": "TKM", "UZB": "UZB", "PNG": "PNG", "VNM": "VNM",
    "THA": "THA", "PAK": "PAK", "BGD": "BGD", "NZL": "NZL", "DEU": "DEU",
    "NLD": "NLD", "FRA": "FRA", "ESP": "ESP",
}
```

### Gold KPI view
Build `gold.kpi_latest` as a single-row view joining the latest values from
all silver tables:
- `brent_price`, `brent_date`, `brent_change` (vs previous day)
- `wti_price`, `wti_date`, `wti_change`
- `us_stocks_mb` (converted from thousand barrels to million barrels),
  `us_stocks_date`, `us_stocks_change_mb`
- `refinery_util_pct`, `refinery_date`, `refinery_change`

---

## Frontend — React

Use **Vite** to scaffold inside `frontend/`. Pin React to **18.x**.

### Theme
Dark theme using MUI `ThemeProvider`:
```javascript
palette: {
  mode: 'dark',
  primary: { main: '#f0a500' },        // amber/gold accent
  background: { default: '#0d1117', paper: '#161b22' },
}
```

### Layout
- Top `AppBar` with title "EIA Oil Dashboard" in primary colour
- Subtitle: "Data source: U.S. Energy Information Administration"
- Responsive MUI Grid layout, `maxWidth="xl"`

### Data loading — IMPORTANT
**Do not load all data in a single `Promise.all` in `App.jsx`.**
Each panel must fetch its own data independently with its own loading and
error state. This way a failure in one panel does not blank the entire
dashboard. Use a custom `useFetch(url)` hook that returns
`{ data, loading, error }` and call it once per panel component.

### Error handling
Each panel component must handle its own error state gracefully — show a
small error message inside the card rather than crashing. Wrap each panel
in a React error boundary so a JavaScript error in one chart cannot crash
the rest of the dashboard.

---

## Dashboard Panels

### 1. KPI Cards (`KpiCards.jsx`)
Four MUI `Card` components in a row (2×2 on mobile, 4×1 on desktop):
- **Brent Price** — USD/barrel + daily change with coloured trend arrow
- **WTI Price** — USD/barrel + daily change with coloured trend arrow
- **US Crude Stocks** — million barrels + week-on-week change
- **Refinery Utilization** — % of operable capacity + week-on-week change

Each card shows: label, big bold value, unit, trend arrow (green up / red
down), and "as of {date}" in small text.

### 2. US Crude Oil Stocks (`CrudeStocksChart.jsx`)
- Recharts `LineChart`
- Two lines: US Total stocks + Cushing Oklahoma stocks
- Date range selector: 1Y / 3Y / 5Y / All
- **5-year seasonal average band**: Do NOT use a single flat average line.
  Instead calculate a proper seasonal reference by computing the average
  value for each week-of-year across the past 5 years, then draw it as a
  dashed reference line that varies week by week. This correctly reflects
  the seasonal pattern in crude stocks.
- Y axis: values in million barrels (divide thousand barrels by 1000)
- Tooltip showing formatted values

### 3. US Monthly Crude Production (`ProductionChart.jsx`)
- Recharts `LineChart`
- Single line: US monthly crude production in thousand barrels/day
- Date range selector: 5Y / 10Y / All

### 4. Top 15 Countries Bar Chart (`TopCountriesChart.jsx`)
- Recharts `BarChart`, horizontal bars
- Top 15 countries by latest available annual production
- Country names on Y axis, values on X axis in thousand barrels/day
- US bar highlighted in primary colour (amber), all others in a neutral blue

### 5. World Choropleth Map (`WorldMap.jsx`)
- React Simple Maps + D3 scale for colour
- Projection: `geoNaturalEarth1`
- Colour scale: `scaleSequentialLog` with `interpolateYlOrRd`
  (light yellow → dark red, log scale handles the large range between
  small and large producers)
- Countries with no data: neutral dark grey `#2c2c2c`
- Hover tooltip showing country name + production value + year
- Colour legend at bottom: Low → High gradient bar + "no data" indicator
- Use the `NUMERIC_TO_ISO3` lookup to convert world-atlas TopoJSON numeric
  IDs to ISO alpha-3 codes for joining with EIA data. Use the full mapping
  from the previous `WorldMap.jsx` (reproduced below).

### NUMERIC_TO_ISO3 mapping for WorldMap.jsx
```javascript
const NUMERIC_TO_ISO3 = {
  "004":"AFG","008":"ALB","012":"DZA","024":"AGO","032":"ARG","036":"AUS",
  "040":"AUT","031":"AZE","050":"BGD","056":"BEL","064":"BTN","068":"BOL",
  "070":"BIH","076":"BRA","100":"BGR","116":"KHM","120":"CMR","124":"CAN",
  "140":"CAF","152":"CHL","156":"CHN","170":"COL","178":"COG","180":"COD",
  "191":"HRV","192":"CUB","196":"CYP","203":"CZE","204":"BEN","208":"DNK",
  "218":"ECU","818":"EGY","222":"SLV","231":"ETH","246":"FIN","250":"FRA",
  "266":"GAB","276":"DEU","288":"GHA","300":"GRC","320":"GTM","324":"GIN",
  "340":"HND","348":"HUN","356":"IND","360":"IDN","364":"IRN","368":"IRQ",
  "372":"IRL","376":"ISR","380":"ITA","392":"JPN","400":"JOR","398":"KAZ",
  "404":"KEN","408":"PRK","410":"KOR","414":"KWT","417":"KGZ","418":"LAO",
  "422":"LBN","426":"LSO","434":"LBY","454":"MWI","458":"MYS","466":"MLI",
  "484":"MEX","496":"MNG","504":"MAR","508":"MOZ","516":"NAM","524":"NPL",
  "528":"NLD","540":"NCL","554":"NZL","558":"NIC","562":"NER","566":"NGA",
  "578":"NOR","586":"PAK","591":"PAN","598":"PNG","600":"PRY","604":"PER",
  "608":"PHL","616":"POL","620":"PRT","630":"PRI","634":"QAT","642":"ROU",
  "643":"RUS","646":"RWA","682":"SAU","686":"SEN","694":"SLE","706":"SOM",
  "710":"ZAF","724":"ESP","728":"SSD","144":"LKA","736":"SDN","752":"SWE",
  "756":"CHE","760":"SYR","762":"TJK","764":"THA","784":"ARE","792":"TUR",
  "795":"TKM","800":"UGA","804":"UKR","826":"GBR","840":"USA","858":"URY",
  "860":"UZB","862":"VEN","704":"VNM","887":"YEM","894":"ZMB","716":"ZWE",
  "470":"MLT","807":"MKD","498":"MDA","051":"ARM","112":"BLR","233":"EST",
  "268":"GEO","428":"LVA","440":"LTU","703":"SVK","705":"SVN","499":"MNE",
  "688":"SRB","020":"AND","096":"BRN",
}
```

---

## README.md

Write a clear README with:
1. Project description and screenshot placeholder
2. Prerequisites: Python 3.11+, Node.js 22.x LTS, EIA API key
   (register free at https://www.eia.gov/opendata/)
3. Setup instructions:
   - Clone repo
   - Copy `.env.example` to `.env` and add EIA API key
   - Install uv if not already installed: `pip install uv`
   - `cd backend && uv sync` (creates venv and installs all dependencies)
   - `uv run python ingestion/run_ingestion.py` (first data load,
     takes a few minutes)
   - `uv run uvicorn main:app --reload`
   - `cd frontend && npm install && npm run dev`
4. How to refresh data: re-run the ingestion script manually
5. Data source credit: U.S. Energy Information Administration

---

## .gitignore

Must include:
```
.env
data/oil_dashboard.duckdb
__pycache__/
*.pyc
node_modules/
frontend/dist/
.venv/
```

---

## Coding Style

- Python: flat, linear scripts — no deep class hierarchies
- Functions must have docstrings and inline comments on non-obvious lines
- No global mutable state except the single shared DuckDB connection
- React: functional components with hooks only
- One responsibility per component file
- No inline styles — use MUI `sx` prop or `createTheme`
