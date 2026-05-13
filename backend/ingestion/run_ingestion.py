"""Manual trigger script -- run this to refresh all data from EIA API.

Usage:
    cd backend
    python ingestion/run_ingestion.py

Steps executed:
    1. Fetch raw data from EIA API into bronze DuckDB tables
    2. Transform bronze -> silver (clean types, normalise columns)
    3. Aggregate silver -> gold (views ready for dashboard API)
"""

import sys
import os

# Allow importing db.py from the parent backend/ directory
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pandas as pd
import duckdb
from fetch_eia import (
    fetch_us_weekly_stocks,
    fetch_cushing_stocks,
    fetch_us_monthly_production,
    fetch_refinery_utilization,
    fetch_international_production,
    fetch_wti_price,
    fetch_brent_price,
)
from db import get_connection

# EIA country code -> ISO 3166-1 alpha-3 mapping for the world map
EIA_TO_ISO3 = {
    "USA": "USA",
    "RUS": "RUS",
    "SAU": "SAU",
    "CAN": "CAN",
    "IRQ": "IRQ",
    "CHN": "CHN",
    "IRN": "IRN",
    "ARE": "ARE",
    "UAE": "ARE",  # EIA sometimes uses UAE
    "BRA": "BRA",
    "KWT": "KWT",
    "MEX": "MEX",
    "KAZ": "KAZ",
    "NGA": "NGA",
    "NOR": "NOR",
    "LBY": "LBY",
    "ALG": "DZA",  # EIA uses ALG, ISO is DZA
    "AGO": "AGO",
    "ANG": "AGO",  # EIA sometimes uses ANG
    "VEN": "VEN",
    "OMN": "OMN",
    "GBR": "GBR",
    "COL": "COL",
    "AZE": "AZE",
    "IDN": "IDN",
    "IND": "IND",
    "MYS": "MYS",
    "ECU": "ECU",
    "ARG": "ARG",
    "QAT": "QAT",
    "GAB": "GAB",
    "COG": "COG",
    "EQG": "GNQ",  # EIA EQG -> ISO GNQ (Equatorial Guinea)
    "GNQ": "GNQ",
    "TTO": "TTO",
    "SSD": "SSD",
    "YEM": "YEM",
    "BRN": "BRN",
    "SYR": "SYR",
    "SDN": "SDN",
    "MRT": "MRT",
    "TCD": "TCD",
    "GHA": "GHA",
    "TZA": "TZA",
    "CMR": "CMR",
    "CIV": "CIV",
    "MOZ": "MOZ",
    "PER": "PER",
    "CHL": "CHL",
    "BOL": "BOL",
    "AUS": "AUS",
    "BHR": "BHR",
    "DEN": "DNK",  # EIA DEN -> ISO DNK (Denmark)
    "DNK": "DNK",
    "ITA": "ITA",
    "EGY": "EGY",
    "ROM": "ROU",  # EIA ROM -> ISO ROU (Romania)
    "CZE": "CZE",
    "HUN": "HUN",
    "POL": "POL",
    "UKR": "UKR",
    "TKM": "TKM",
    "UZB": "UZB",
    "PNG": "PNG",
    "VNM": "VNM",
    "THA": "THA",
    "PAK": "PAK",
    "BGD": "BGD",
    "NZL": "NZL",
    "DEU": "DEU",
    "NLD": "NLD",
    "FRA": "FRA",
    "ESP": "ESP",
}


# ─── Bronze layer ─────────────────────────────────────────────────────────────

def load_bronze(conn: duckdb.DuckDBPyConnection) -> None:
    """Fetch all series from EIA API and write raw data to bronze tables."""
    print("\n=== BRONZE: Fetching raw data from EIA API ===")

    _write_bronze_stocks(conn)
    _write_bronze_cushing(conn)
    _write_bronze_production(conn)
    _write_bronze_refinery(conn)
    _write_bronze_international(conn)
    _write_bronze_prices(conn)


def _write_bronze_stocks(conn: duckdb.DuckDBPyConnection) -> None:
    rows = fetch_us_weekly_stocks()
    df = pd.DataFrame(rows)
    conn.execute("DROP TABLE IF EXISTS bronze.us_weekly_stocks")
    conn.execute("CREATE TABLE bronze.us_weekly_stocks AS SELECT * FROM df")
    print(f"    -> bronze.us_weekly_stocks: {len(df)} rows")


def _write_bronze_cushing(conn: duckdb.DuckDBPyConnection) -> None:
    rows = fetch_cushing_stocks()
    df = pd.DataFrame(rows)
    conn.execute("DROP TABLE IF EXISTS bronze.cushing_stocks")
    conn.execute("CREATE TABLE bronze.cushing_stocks AS SELECT * FROM df")
    print(f"    -> bronze.cushing_stocks: {len(df)} rows")


def _write_bronze_production(conn: duckdb.DuckDBPyConnection) -> None:
    rows = fetch_us_monthly_production()
    df = pd.DataFrame(rows)
    conn.execute("DROP TABLE IF EXISTS bronze.us_monthly_production")
    conn.execute("CREATE TABLE bronze.us_monthly_production AS SELECT * FROM df")
    print(f"    -> bronze.us_monthly_production: {len(df)} rows")


def _write_bronze_refinery(conn: duckdb.DuckDBPyConnection) -> None:
    rows = fetch_refinery_utilization()
    df = pd.DataFrame(rows)
    conn.execute("DROP TABLE IF EXISTS bronze.refinery_utilization")
    conn.execute("CREATE TABLE bronze.refinery_utilization AS SELECT * FROM df")
    print(f"    -> bronze.refinery_utilization: {len(df)} rows")


def _write_bronze_international(conn: duckdb.DuckDBPyConnection) -> None:
    rows = fetch_international_production()
    df = pd.DataFrame(rows)
    conn.execute("DROP TABLE IF EXISTS bronze.international_production")
    conn.execute("CREATE TABLE bronze.international_production AS SELECT * FROM df")
    print(f"    -> bronze.international_production: {len(df)} rows")


def _write_bronze_prices(conn: duckdb.DuckDBPyConnection) -> None:
    wti_rows = fetch_wti_price()
    brent_rows = fetch_brent_price()
    wti_df = pd.DataFrame(wti_rows)
    brent_df = pd.DataFrame(brent_rows)
    combined = pd.concat([wti_df, brent_df], ignore_index=True)
    conn.execute("DROP TABLE IF EXISTS bronze.crude_prices")
    conn.execute("CREATE TABLE bronze.crude_prices AS SELECT * FROM combined")
    print(f"    -> bronze.crude_prices: {len(combined)} rows (WTI + Brent)")


# ─── Silver layer ─────────────────────────────────────────────────────────────

def load_silver(conn: duckdb.DuckDBPyConnection) -> None:
    """Transform bronze tables into clean silver tables."""
    print("\n=== SILVER: Cleaning and normalising data ===")

    _silver_stocks(conn)
    _silver_cushing(conn)
    _silver_production(conn)
    _silver_refinery(conn)
    _silver_international(conn)
    _silver_prices(conn)


def _silver_stocks(conn: duckdb.DuckDBPyConnection) -> None:
    conn.execute("DROP TABLE IF EXISTS silver.us_weekly_stocks")
    conn.execute("""
        CREATE TABLE silver.us_weekly_stocks AS
        SELECT
            CAST(period AS DATE)               AS date,
            TRY_CAST(value AS DOUBLE)          AS value_kb,
            'thousand barrels'                 AS unit
        FROM bronze.us_weekly_stocks
        WHERE TRY_CAST(value AS DOUBLE) IS NOT NULL
          AND TRY_CAST(value AS DOUBLE) > 0
        ORDER BY date
    """)
    count = conn.execute("SELECT COUNT(*) FROM silver.us_weekly_stocks").fetchone()[0]
    print(f"    -> silver.us_weekly_stocks: {count} rows")


def _silver_cushing(conn: duckdb.DuckDBPyConnection) -> None:
    conn.execute("DROP TABLE IF EXISTS silver.cushing_stocks")
    conn.execute("""
        CREATE TABLE silver.cushing_stocks AS
        SELECT
            CAST(period AS DATE)               AS date,
            TRY_CAST(value AS DOUBLE)          AS value_kb,
            'thousand barrels'                 AS unit
        FROM bronze.cushing_stocks
        WHERE TRY_CAST(value AS DOUBLE) IS NOT NULL
          AND TRY_CAST(value AS DOUBLE) > 0
        ORDER BY date
    """)
    count = conn.execute("SELECT COUNT(*) FROM silver.cushing_stocks").fetchone()[0]
    print(f"    -> silver.cushing_stocks: {count} rows")


def _silver_production(conn: duckdb.DuckDBPyConnection) -> None:
    conn.execute("DROP TABLE IF EXISTS silver.us_monthly_production")
    # EIA monthly production period format: YYYY-MM
    conn.execute("""
        CREATE TABLE silver.us_monthly_production AS
        SELECT
            CAST(period || '-01' AS DATE)      AS date,
            TRY_CAST(value AS DOUBLE)          AS value_kbd,
            'thousand barrels per day'         AS unit
        FROM bronze.us_monthly_production
        WHERE TRY_CAST(value AS DOUBLE) IS NOT NULL
          AND TRY_CAST(value AS DOUBLE) > 0
        ORDER BY date
    """)
    count = conn.execute("SELECT COUNT(*) FROM silver.us_monthly_production").fetchone()[0]
    print(f"    -> silver.us_monthly_production: {count} rows")


def _silver_refinery(conn: duckdb.DuckDBPyConnection) -> None:
    conn.execute("DROP TABLE IF EXISTS silver.refinery_utilization")
    # bronze.refinery_utilization is already filtered to WPULEUS3 (national utilization %)
    conn.execute("""
        CREATE TABLE silver.refinery_utilization AS
        SELECT
            CAST(period AS DATE)               AS date,
            TRY_CAST(value AS DOUBLE)          AS value_pct,
            'percent of operable capacity'     AS unit
        FROM bronze.refinery_utilization
        WHERE TRY_CAST(value AS DOUBLE) IS NOT NULL
          AND TRY_CAST(value AS DOUBLE) > 0
        ORDER BY date
    """)
    count = conn.execute("SELECT COUNT(*) FROM silver.refinery_utilization").fetchone()[0]
    print(f"    -> silver.refinery_utilization: {count} rows")


def _silver_international(conn: duckdb.DuckDBPyConnection) -> None:
    conn.execute("DROP TABLE IF EXISTS silver.international_production")

    # EIA international/data/ returns ISO 3166-1 alpha-3 codes directly in countryRegionId.
    # No complex mapping needed -- we use countryRegionId as iso3 directly.
    # A small override table handles the rare cases that differ (e.g. Kosovo XKX).
    override_rows = ", ".join(
        f"('{eia}', '{iso}')" for eia, iso in EIA_TO_ISO3.items()
    )

    conn.execute("CREATE OR REPLACE TEMP TABLE eia_iso_map (eia_code VARCHAR, iso3 VARCHAR)")
    conn.execute(f"INSERT INTO eia_iso_map VALUES {override_rows}")

    # Identify the country column name (may be countryRegionId or countryRegionid)
    cols = [r[0] for r in conn.execute("DESCRIBE bronze.international_production").fetchall()]
    country_col = next(
        (c for c in cols if c.lower() in ("countryregionid",)),
        "countryRegionId",
    )
    name_col = next(
        (c for c in cols if c.lower() in ("countryregionname",)),
        None,
    )

    name_expr = f'b."{name_col}"' if name_col else f'b."{country_col}"'

    conn.execute(f"""
        CREATE TABLE silver.international_production AS
        SELECT
            CAST(b.period AS INTEGER)                       AS year,
            b."{country_col}"                               AS eia_country_code,
            {name_expr}                                     AS country_name,
            TRY_CAST(b.value AS DOUBLE)                     AS value_kbd,
            'thousand barrels per day'                      AS unit,
            COALESCE(m.iso3, b."{country_col}")             AS iso3
        FROM bronze.international_production b
        LEFT JOIN eia_iso_map m ON m.eia_code = b."{country_col}"
        WHERE TRY_CAST(b.value AS DOUBLE) IS NOT NULL
          AND TRY_CAST(b.value AS DOUBLE) > 0
        ORDER BY year DESC, value_kbd DESC
    """)
    count = conn.execute("SELECT COUNT(*) FROM silver.international_production").fetchone()[0]
    print(f"    -> silver.international_production: {count} rows")


def _silver_prices(conn: duckdb.DuckDBPyConnection) -> None:
    conn.execute("DROP TABLE IF EXISTS silver.crude_prices")
    conn.execute("""
        CREATE TABLE silver.crude_prices AS
        SELECT
            CAST(period AS DATE)               AS date,
            series                             AS series_code,
            CASE series
                WHEN 'RWTC'  THEN 'WTI'
                WHEN 'RBRTE' THEN 'Brent'
                ELSE series
            END                                AS price_type,
            TRY_CAST(value AS DOUBLE)          AS value_usd,
            'dollars per barrel'               AS unit
        FROM bronze.crude_prices
        WHERE TRY_CAST(value AS DOUBLE) IS NOT NULL
          AND TRY_CAST(value AS DOUBLE) > 0
        ORDER BY date DESC
    """)
    count = conn.execute("SELECT COUNT(*) FROM silver.crude_prices").fetchone()[0]
    print(f"    -> silver.crude_prices: {count} rows")


# ─── Gold layer ───────────────────────────────────────────────────────────────

def load_gold(conn: duckdb.DuckDBPyConnection) -> None:
    """Create gold-layer views aggregated for each dashboard panel."""
    print("\n=== GOLD: Building dashboard views ===")

    _gold_kpi(conn)
    _gold_stocks_timeseries(conn)
    _gold_production_timeseries(conn)
    _gold_top_countries(conn)
    _gold_world_map(conn)


def _gold_kpi(conn: duckdb.DuckDBPyConnection) -> None:
    conn.execute("DROP VIEW IF EXISTS gold.kpi_latest")
    conn.execute("""
        CREATE VIEW gold.kpi_latest AS
        WITH brent AS (
            SELECT value_usd, date
            FROM silver.crude_prices
            WHERE price_type = 'Brent'
            ORDER BY date DESC LIMIT 2
        ),
        wti AS (
            SELECT value_usd, date
            FROM silver.crude_prices
            WHERE price_type = 'WTI'
            ORDER BY date DESC LIMIT 2
        ),
        stocks AS (
            SELECT value_kb, date
            FROM silver.us_weekly_stocks
            ORDER BY date DESC LIMIT 2
        ),
        refinery AS (
            SELECT value_pct, date
            FROM silver.refinery_utilization
            ORDER BY date DESC LIMIT 2
        )
        SELECT
            (SELECT value_usd FROM brent LIMIT 1)                             AS brent_price,
            (SELECT date      FROM brent LIMIT 1)                             AS brent_date,
            (SELECT value_usd FROM brent LIMIT 1) -
                (SELECT value_usd FROM brent OFFSET 1 LIMIT 1)               AS brent_change,
            (SELECT value_usd FROM wti LIMIT 1)                               AS wti_price,
            (SELECT date      FROM wti LIMIT 1)                               AS wti_date,
            (SELECT value_usd FROM wti LIMIT 1) -
                (SELECT value_usd FROM wti OFFSET 1 LIMIT 1)                 AS wti_change,
            ROUND((SELECT value_kb FROM stocks LIMIT 1) / 1000.0, 1)         AS us_stocks_mb,
            (SELECT date FROM stocks LIMIT 1)                                 AS us_stocks_date,
            ROUND(
                ((SELECT value_kb FROM stocks LIMIT 1) -
                 (SELECT value_kb FROM stocks OFFSET 1 LIMIT 1)) / 1000.0, 1
            )                                                                 AS us_stocks_change_mb,
            (SELECT value_pct FROM refinery LIMIT 1)                         AS refinery_util_pct,
            (SELECT date FROM refinery LIMIT 1)                              AS refinery_date,
            (SELECT value_pct FROM refinery LIMIT 1) -
                (SELECT value_pct FROM refinery OFFSET 1 LIMIT 1)            AS refinery_change
    """)
    print("    -> gold.kpi_latest view created")


def _gold_stocks_timeseries(conn: duckdb.DuckDBPyConnection) -> None:
    conn.execute("DROP VIEW IF EXISTS gold.stocks_timeseries")
    conn.execute("""
        CREATE VIEW gold.stocks_timeseries AS
        SELECT
            s.date,
            s.value_kb                         AS us_stocks_kb,
            c.value_kb                         AS cushing_stocks_kb
        FROM silver.us_weekly_stocks s
        LEFT JOIN silver.cushing_stocks c ON c.date = s.date
        ORDER BY s.date
    """)
    print("    -> gold.stocks_timeseries view created")


def _gold_production_timeseries(conn: duckdb.DuckDBPyConnection) -> None:
    conn.execute("DROP VIEW IF EXISTS gold.production_timeseries")
    conn.execute("""
        CREATE VIEW gold.production_timeseries AS
        SELECT
            date,
            value_kbd                          AS production_kbd
        FROM silver.us_monthly_production
        ORDER BY date
    """)
    print("    -> gold.production_timeseries view created")


def _gold_top_countries(conn: duckdb.DuckDBPyConnection) -> None:
    conn.execute("DROP VIEW IF EXISTS gold.top_countries")
    conn.execute("""
        CREATE VIEW gold.top_countries AS
        WITH latest_year AS (
            SELECT MAX(year) AS yr FROM silver.international_production
        ),
        ranked AS (
            SELECT
                p.country_name,
                p.eia_country_code,
                p.iso3,
                p.value_kbd,
                p.year
            FROM silver.international_production p
            JOIN latest_year ly ON p.year = ly.yr
            -- Exclude aggregates (OPEC, OECD, World totals)
            WHERE LENGTH(p.eia_country_code) = 3
              AND p.eia_country_code NOT IN ('OPE', 'OEC', 'WOR', 'NON', 'NAM', 'CAM', 'SAM', 'EUR', 'MEA', 'AFR', 'ASI', 'OCN')
            ORDER BY p.value_kbd DESC
            LIMIT 15
        )
        SELECT * FROM ranked
    """)
    print("    -> gold.top_countries view created")


def _gold_world_map(conn: duckdb.DuckDBPyConnection) -> None:
    conn.execute("DROP VIEW IF EXISTS gold.world_production_map")
    conn.execute("""
        CREATE VIEW gold.world_production_map AS
        WITH latest_year AS (
            SELECT MAX(year) AS yr FROM silver.international_production
        )
        SELECT
            p.iso3,
            p.country_name,
            p.eia_country_code,
            p.value_kbd,
            p.year
        FROM silver.international_production p
        JOIN latest_year ly ON p.year = ly.yr
        WHERE LENGTH(p.eia_country_code) = 3
          AND p.eia_country_code NOT IN ('OPE', 'OEC', 'WOR', 'NON', 'NAM', 'CAM', 'SAM', 'EUR', 'MEA', 'AFR', 'ASI', 'OCN')
          AND p.iso3 IS NOT NULL
        ORDER BY p.value_kbd DESC
    """)
    print("    -> gold.world_production_map view created")


# ─── Entry point ──────────────────────────────────────────────────────────────

def main() -> None:
    """Run the full ingestion pipeline: fetch -> bronze -> silver -> gold."""
    print("EIA Oil Dashboard -- Data Ingestion")
    print("====================================")

    conn = get_connection()
    try:
        load_bronze(conn)
        load_silver(conn)
        load_gold(conn)
        print("\nIngestion complete. Dashboard data is ready.")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
