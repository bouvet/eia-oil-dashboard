"""FastAPI app — all dashboard API routes.

Each endpoint queries DuckDB gold-layer views and returns JSON.
Run with: uvicorn main:app --reload
"""

import math
import pandas as pd
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
import duckdb

from db import get_connection, query_to_records

app = FastAPI(title="EIA Oil Dashboard API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174", "http://localhost:5175"],  # Vite dev ports
    allow_methods=["GET"],
    allow_headers=["*"],
)


def _serialize_row(row: dict) -> dict:
    """Convert pandas Timestamps and any remaining NaN to JSON-safe types."""
    out = {}
    for k, v in row.items():
        if isinstance(v, pd.Timestamp):
            out[k] = v.date().isoformat()
        elif isinstance(v, float) and math.isnan(v):
            out[k] = None
        else:
            out[k] = v
    return out


def get_db():
    """FastAPI dependency that yields a DuckDB connection and closes it after use."""
    conn = get_connection()
    try:
        yield conn
    finally:
        conn.close()


@app.get("/api/kpi")
def get_kpi(conn: duckdb.DuckDBPyConnection = Depends(get_db)):
    """Return the latest KPI values: prices, stocks, production, utilization.

    Single-row response with all headline figures.
    """
    rows = query_to_records(conn, "SELECT * FROM gold.kpi_latest")
    if not rows:
        return {}
    return _serialize_row(rows[0])


@app.get("/api/stocks")
def get_stocks(conn: duckdb.DuckDBPyConnection = Depends(get_db)):
    """Return weekly US crude stocks time series.

    Each row: { date, us_stocks_kb, cushing_stocks_kb }
    """
    rows = query_to_records(conn, "SELECT * FROM gold.stocks_timeseries ORDER BY date")
    return [_serialize_row(r) for r in rows]


@app.get("/api/production")
def get_production(conn: duckdb.DuckDBPyConnection = Depends(get_db)):
    """Return monthly US crude production time series.

    Each row: { date, production_kbd }
    """
    rows = query_to_records(conn, "SELECT * FROM gold.production_timeseries ORDER BY date")
    return [_serialize_row(r) for r in rows]


@app.get("/api/countries")
def get_countries(conn: duckdb.DuckDBPyConnection = Depends(get_db)):
    """Return top 15 countries by latest annual crude production.

    Each row: { country_name, iso3, value_kbd, year }
    """
    rows = query_to_records(
        conn,
        "SELECT country_name, iso3, value_kbd, year FROM gold.top_countries ORDER BY value_kbd DESC",
    )
    return rows


@app.get("/api/world")
def get_world(conn: duckdb.DuckDBPyConnection = Depends(get_db)):
    """Return all countries with latest production value for the choropleth map.

    Each row: { iso3, country_name, value_kbd, year }
    """
    rows = query_to_records(
        conn,
        "SELECT iso3, country_name, value_kbd, year FROM gold.world_production_map",
    )
    return rows
