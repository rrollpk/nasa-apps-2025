import httpx, orjson
from typing import Dict
from .config import (
    AQ_URL,
    WX_ARCHIVE_URL,
    TIMEOUT_S,
    TIMEZONE,
    HOURLY_AQ_VARS,
    HOURLY_WX_VARS,
)


def make_client(max_connections: int, max_keepalive: int) -> httpx.AsyncClient:
    limits = httpx.Limits(
        max_connections=max_connections, max_keepalive_connections=max_keepalive
    )
    return httpx.AsyncClient(limits=limits, timeout=TIMEOUT_S)


async def _get_json(client: httpx.AsyncClient, url: str, params: dict) -> Dict:
    r = await client.get(url, params=params)
    r.raise_for_status()
    return orjson.loads(r.content)


async def fetch_aq(
    client: httpx.AsyncClient,
    lat: float,
    lon: float,
    past_days: int,
    forecast_days: int,
) -> Dict:
    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": ",".join(HOURLY_AQ_VARS),
        "current": ",".join(HOURLY_AQ_VARS),
        "past_days": past_days,
        "forecast_days": forecast_days,
        "timezone": TIMEZONE,
    }
    return await _get_json(client, AQ_URL, params)


async def fetch_weather_history(
    client: httpx.AsyncClient, lat: float, lon: float, start_date: str, end_date: str
) -> Dict:
    params = {
        "latitude": lat,
        "longitude": lon,
        "start_date": start_date,
        "end_date": end_date,
        "hourly": ",".join(HOURLY_WX_VARS),
        "timezone": TIMEZONE,
    }
    return await _get_json(client, WX_ARCHIVE_URL, params)
