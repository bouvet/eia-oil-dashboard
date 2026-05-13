"""All EIA API v2 fetch functions.

Each function fetches a specific series from the EIA API, handles pagination,
and returns a list of row dicts ready to be inserted into DuckDB.

Verified endpoint paths and series codes as of 2026-05:
  Stocks:         petroleum/stoc/wstk/data/
  Production:     petroleum/crd/crpdn/data/
  Refinery util:  petroleum/pnp/wiup/data/
  Prices:         petroleum/pri/spt/data/
  International:  international/data/
"""

import os
import time
import requests
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", "..", ".env"))

EIA_BASE = "https://api.eia.gov/v2"
PAGE_SIZE = 5000
REQUEST_DELAY = 0.25  # seconds between requests to be a good API citizen


def _get_api_key() -> str:
    """Read the EIA API key from the environment."""
    key = os.getenv("EIA_API_KEY")
    if not key:
        raise EnvironmentError("EIA_API_KEY not found. Copy .env.example to .env and set your key.")
    return key


def _fetch_all_pages(endpoint: str, params: dict) -> list[dict]:
    """Fetch all pages from an EIA API endpoint using offset pagination.

    Returns the combined list of row dicts from every page.
    """
    api_key = _get_api_key()
    params = dict(params)
    params["api_key"] = api_key
    params["length"] = PAGE_SIZE
    params["offset"] = 0

    all_rows = []
    while True:
        url = f"{EIA_BASE}/{endpoint}"
        resp = requests.get(url, params=params, timeout=30)
        resp.raise_for_status()
        body = resp.json()

        rows = body.get("response", {}).get("data", [])
        all_rows.extend(rows)

        total = body.get("response", {}).get("total", 0)
        params["offset"] += PAGE_SIZE

        if params["offset"] >= int(total):
            break

        time.sleep(REQUEST_DELAY)

    return all_rows


def fetch_us_weekly_stocks() -> list[dict]:
    """Fetch US weekly commercial crude oil stocks (excl. SPR).

    Series: WCESTUS1 via petroleum/stoc/wstk/data/.
    Unit: thousand barrels (MBBL in EIA notation).
    Returns list of dicts with keys: period, value, series-description, units.
    """
    print("  Fetching US weekly crude stocks...")
    return _fetch_all_pages(
        "petroleum/stoc/wstk/data/",
        {
            "frequency": "weekly",
            "data[]": "value",
            "facets[series][]": "WCESTUS1",
            "sort[0][column]": "period",
            "sort[0][direction]": "desc",
        },
    )


def fetch_cushing_stocks() -> list[dict]:
    """Fetch Cushing Oklahoma crude oil stocks.

    Series: W_EPC0_SAX_YCUOK_MBBL via petroleum/stoc/wstk/data/.
    Cushing is the WTI delivery point, closely watched by traders.
    Unit: thousand barrels.
    """
    print("  Fetching Cushing Oklahoma crude stocks...")
    return _fetch_all_pages(
        "petroleum/stoc/wstk/data/",
        {
            "frequency": "weekly",
            "data[]": "value",
            "facets[series][]": "W_EPC0_SAX_YCUOK_MBBL",
            "sort[0][column]": "period",
            "sort[0][direction]": "desc",
        },
    )


def fetch_us_monthly_production() -> list[dict]:
    """Fetch US monthly crude oil field production in thousand barrels/day.

    Series: MCRFPUS2 via petroleum/crd/crpdn/data/.
    Facets: duoarea=NUS (National US), product=EPC0 (crude oil).
    """
    print("  Fetching US monthly crude production...")
    return _fetch_all_pages(
        "petroleum/crd/crpdn/data/",
        {
            "frequency": "monthly",
            "data[]": "value",
            "facets[duoarea][]": "NUS",
            "facets[product][]": "EPC0",
            "facets[series][]": "MCRFPUS2",  # kbd series; MCRFPUS1 is total monthly bbls
            "sort[0][column]": "period",
            "sort[0][direction]": "desc",
        },
    )


def fetch_refinery_utilization() -> list[dict]:
    """Fetch US weekly refinery utilization rate.

    Series: WPULEUS3 (Percent Utilization of Refinery Operable Capacity)
    via petroleum/pnp/wiup/data/. Unit: %.
    """
    print("  Fetching weekly refinery utilization...")
    return _fetch_all_pages(
        "petroleum/pnp/wiup/data/",
        {
            "frequency": "weekly",
            "data[]": "value",
            "facets[series][]": "WPULEUS3",
            "sort[0][column]": "period",
            "sort[0][direction]": "desc",
        },
    )


def fetch_international_production() -> list[dict]:
    """Fetch international annual crude oil production by country.

    Facets: productId=55 (crude oil incl. lease condensate), activityId=1 (production).
    Country codes in the response are ISO 3166-1 alpha-3.
    Unit: TBPD (thousand barrels per day).
    """
    print("  Fetching international annual crude production...")
    return _fetch_all_pages(
        "international/data/",
        {
            "frequency": "annual",
            "data[]": "value",
            "facets[productId][]": "55",
            "facets[activityId][]": "1",
            "sort[0][column]": "period",
            "sort[0][direction]": "desc",
        },
    )


def fetch_wti_price() -> list[dict]:
    """Fetch WTI crude oil spot price (daily).

    Series: RWTC — West Texas Intermediate, USD per barrel.
    Returns list of dicts with keys: period, value, series-description.
    """
    print("  Fetching WTI spot price...")
    return _fetch_all_pages(
        "petroleum/pri/spt/data/",
        {
            "frequency": "daily",
            "data[]": "value",
            "facets[series][]": "RWTC",
            "sort[0][column]": "period",
            "sort[0][direction]": "desc",
        },
    )


def fetch_brent_price() -> list[dict]:
    """Fetch Brent crude oil spot price (daily).

    Series: RBRTE — Europe Brent Spot Price FOB, USD per barrel.
    Returns list of dicts with keys: period, value, series-description.
    """
    print("  Fetching Brent spot price...")
    return _fetch_all_pages(
        "petroleum/pri/spt/data/",
        {
            "frequency": "daily",
            "data[]": "value",
            "facets[series][]": "RBRTE",
            "sort[0][column]": "period",
            "sort[0][direction]": "desc",
        },
    )
