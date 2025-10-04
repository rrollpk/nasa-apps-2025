import asyncio, orjson
import polars as pl
from typing import List, Optional, Tuple
from datetime import date, timedelta
from .registry import coords_for_keys
from .client import make_client, fetch_aq, fetch_weather_history
from .config import (
    MAX_CONNECTIONS,
    MAX_KEEPALIVE,
    HW_PAST_DAYS,
    AQ_PAST_DAYS,
    AQ_FORECAST_DAYS,
)


def _resolve_dates(
    start: Optional[str], end: Optional[str], days: int
) -> Tuple[str, str]:
    if start and end:
        return start, end
    if start and not end:
        return start, date.today().isoformat()
    if not start and end:
        d_end = date.fromisoformat(end)
        d_start = d_end - timedelta(days=days)
        return d_start.isoformat(), end
    d_end = date.today()
    d_start = d_end - timedelta(days=days)
    return d_start.isoformat(), d_end.isoformat()


async def _fetch_pair(
    client,
    row,
    start_date: str,
    end_date: str,
    aq_past_days: int,
    aq_forecast_days: int,
):
    lat, lon = row["latitud"], row["longitud"]
    aq_task = fetch_aq(
        client, lat, lon, past_days=aq_past_days, forecast_days=aq_forecast_days
    )
    wx_task = fetch_weather_history(client, lat, lon, start_date, end_date)
    return await asyncio.gather(aq_task, wx_task)


async def fetch_for_keys(
    registry: pl.DataFrame,
    keys: List[str],
    start: Optional[str] = None,
    end: Optional[str] = None,
    days: int = HW_PAST_DAYS,
    # NEW: AQ window (defaults from config)
    aq_past_days: int = AQ_PAST_DAYS,
    aq_forecast_days: int = AQ_FORECAST_DAYS,
) -> bytes:
    coords = coords_for_keys(registry, keys)
    start_date, end_date = _resolve_dates(start, end, days)

    async with make_client(MAX_CONNECTIONS, MAX_KEEPALIVE) as client:
        tasks = [
            _fetch_pair(
                client, row, start_date, end_date, aq_past_days, aq_forecast_days
            )
            for row in coords.iter_rows(named=True)
        ]
        results = await asyncio.gather(*tasks)

    payload = []
    for row, (aq, wx) in zip(coords.iter_rows(named=True), results):
        payload.append(
            {
                "key": row["key"],
                "comunidad": row["comunidad"],
                "provincia": row["provincia"],
                "poblacion": row["poblacion"],
                "coords": {
                    "lat": row["latitud"],
                    "lon": row["longitud"],
                    "alt": row["altitud"],
                },
                "open_meteo": aq,  # AQ: includes current + past_days + forecast_days
                "open_meteo_weather": {
                    "start_date": start_date,
                    "end_date": end_date,
                    **wx,
                },
            }
        )
    return orjson.dumps(payload)


async def fetch_for_keys_batched(
    registry: pl.DataFrame,
    keys: List[str],
    batch_size: int = 400,
    inter_batch_sleep: float = 0.2,
    start: Optional[str] = None,
    end: Optional[str] = None,
    days: int = HW_PAST_DAYS,
    aq_past_days: int = AQ_PAST_DAYS,
    aq_forecast_days: int = AQ_FORECAST_DAYS,
) -> bytes:
    coords = coords_for_keys(registry, keys)
    start_date, end_date = _resolve_dates(start, end, days)
    payload = []

    async with make_client(MAX_CONNECTIONS, MAX_KEEPALIVE) as client:
        for i in range(0, coords.height, batch_size):
            chunk = coords.slice(i, batch_size)
            tasks = [
                _fetch_pair(
                    client, row, start_date, end_date, aq_past_days, aq_forecast_days
                )
                for row in chunk.iter_rows(named=True)
            ]
            results = await asyncio.gather(*tasks)

            for row, (aq, wx) in zip(chunk.iter_rows(named=True), results):
                payload.append(
                    {
                        "key": row["key"],
                        "comunidad": row["comunidad"],
                        "provincia": row["provincia"],
                        "poblacion": row["poblacion"],
                        "coords": {
                            "lat": row["latitud"],
                            "lon": row["longitud"],
                            "alt": row["altitud"],
                        },
                        "open_meteo": aq,
                        "open_meteo_weather": {
                            "start_date": start_date,
                            "end_date": end_date,
                            **wx,
                        },
                    }
                )

            if inter_batch_sleep and i + batch_size < coords.height:
                await asyncio.sleep(inter_batch_sleep)

    return orjson.dumps(payload)
