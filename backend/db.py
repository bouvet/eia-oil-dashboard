"""DuckDB connection and query helpers."""

import os
import duckdb
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "data" / "oil_dashboard.duckdb"


def get_connection() -> duckdb.DuckDBPyConnection:
    """Return a DuckDB connection to the dashboard database.

    Creates the data directory if it doesn't exist.
    """
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = duckdb.connect(str(DB_PATH))
    _ensure_schemas(conn)
    return conn


def _ensure_schemas(conn: duckdb.DuckDBPyConnection) -> None:
    """Create bronze/silver/gold schemas if they don't exist yet."""
    for schema in ("bronze", "silver", "gold"):
        conn.execute(f"CREATE SCHEMA IF NOT EXISTS {schema}")


def query_to_records(conn: duckdb.DuckDBPyConnection, sql: str) -> list[dict]:
    """Run a SQL query and return results as a list of dicts.

    Converts NaN/NaT to None so results are JSON-serialisable.
    """
    import math
    result = conn.execute(sql).fetchdf()
    records = result.where(result.notna(), other=None).to_dict(orient="records")
    # float NaN survives .where() for object-dtype columns; scrub them
    for row in records:
        for k, v in row.items():
            if isinstance(v, float) and math.isnan(v):
                row[k] = None
    return records
