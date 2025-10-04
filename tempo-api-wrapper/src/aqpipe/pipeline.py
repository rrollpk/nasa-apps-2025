import asyncio, orjson
import polars as pl
from typing import List
from .registry import coords_for_keys
from .client import make_client, fetch_aq
from .config import MAX_CONNECTIONS, MAX_KEEPALIVE


async def fetch_for_keys(registry: pl.DataFrame, keys: List[str]) -> bytes:
    """
    1) resolve key -> coords
    2) fetch Open-Meteo AQ for each
    3) return compact JSON (bytes)
    """
    coords = coords_for_keys(registry, keys)

    async with make_client(MAX_CONNECTIONS, MAX_KEEPALIVE) as client:
        tasks = [
            fetch_aq(client, row["latitud"], row["longitud"])
            for row in coords.iter_rows(named=True)
        ]
        results = await asyncio.gather(*tasks)

    payload = []
    for row, data in zip(coords.iter_rows(named=True), results):
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
                "open_meteo": data,
            }
        )
    return orjson.dumps(payload)


# batched variant for rate limits
async def fetch_for_keys_batched(
    registry: pl.DataFrame,
    keys: List[str],
    batch_size: int = 400,
    inter_batch_sleep: float = 0.2,
) -> bytes:
    coords = coords_for_keys(registry, keys)
    payload = []

    async with make_client(MAX_CONNECTIONS, MAX_KEEPALIVE) as client:
        for start in range(0, coords.height, batch_size):
            chunk = coords.slice(start, batch_size)
            tasks = [
                fetch_aq(client, r["latitud"], r["longitud"])
                for r in chunk.iter_rows(named=True)
            ]
            results = await asyncio.gather(*tasks)

            for row, data in zip(chunk.iter_rows(named=True), results):
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
                        "open_meteo": data,
                    }
                )
            if inter_batch_sleep and start + batch_size < coords.height:
                await asyncio.sleep(inter_batch_sleep)

    return orjson.dumps(payload)
