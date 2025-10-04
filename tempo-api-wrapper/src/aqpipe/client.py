import httpx, orjson
from typing import Dict
from .config import AQ_URL, TIMEOUT_S, HOURLY_VARS, CURRENT_VARS, TIMEZONE


async def fetch_aq(client: httpx.AsyncClient, lat: float, lon: float) -> Dict:
    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": ",".join(HOURLY_VARS),
        "current": ",".join(CURRENT_VARS),
        "timezone": TIMEZONE,
    }
    r = await client.get(AQ_URL, params=params, timeout=TIMEOUT_S)
    r.raise_for_status()
    return orjson.loads(r.content)


def make_client(max_connections: int, max_keepalive: int) -> httpx.AsyncClient:
    limits = httpx.Limits(
        max_connections=max_connections, max_keepalive_connections=max_keepalive
    )
    return httpx.AsyncClient(limits=limits)
