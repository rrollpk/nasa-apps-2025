from pathlib import Path
import polars as pl
from .keys import make_key

# map many possible header spellings -> canonical
COLMAP = {
    "comunidad": "comunidad",
    "comunidadautonoma": "comunidad",
    "provincia": "provincia",
    "poblacion": "poblacion",
    "población": "poblacion",  # accented header
    "latitud": "latitud",
    "longitud": "longitud",
    "altitud": "altitud",
    "habitantes": "habitantes",
    "hombres": "hombres",
    "mujeres": "mujeres",
}


def _canonicalize_headers(cols: list[str]) -> list[str]:
    out = []
    for c in cols:
        k = c.strip().lower()
        k = k.replace(" ", "")  # tolerate spaces
        # also tolerate BOM or weird chars
        k = k.replace("\ufeff", "")
        out.append(COLMAP.get(k, k))  # fallback to original if unknown
    return out


def load_registry(csv_path: str | Path) -> pl.DataFrame:
    # Read as UTF-8; if your file is tab-separated, pass separator="\t"
    df = pl.read_csv(csv_path, infer_schema_length=1000, encoding="utf8")

    # Rename columns to our canonical names
    df = df.rename(dict(zip(df.columns, _canonicalize_headers(df.columns))))

    # Validate required columns exist
    required = {"comunidad", "provincia", "poblacion", "latitud", "longitud", "altitud"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    # Cast dtypes and build the composite key
    df = df.with_columns(
        [
            pl.col("comunidad").cast(pl.Utf8),
            pl.col("provincia").cast(pl.Utf8),
            pl.col("poblacion").cast(pl.Utf8),
            pl.col("latitud").cast(pl.Float64),
            pl.col("longitud").cast(pl.Float64),
            pl.col("altitud").cast(pl.Float64),
        ]
    ).with_columns(
        pl.struct(["comunidad", "provincia", "poblacion"])
        .map_elements(
            lambda row: make_key(row["comunidad"], row["provincia"], row["poblacion"])
        )
        .alias("key")
    )

    # Uniqueness check
    dups = df.group_by("key").agg(pl.len().alias("n")).filter(pl.col("n") > 1)
    if dups.height:
        sample = dups.head(5).select("key", "n").to_dict(as_series=False)
        raise ValueError(f"Duplicate keys in registry (first few): {sample}")

    return df.select(
        "key", "comunidad", "provincia", "poblacion", "latitud", "longitud", "altitud"
    )


def coords_for_keys(registry: pl.DataFrame, keys: list[str]) -> pl.DataFrame:
    """
    Return coords for each input key (keeps input order, errors on missing).
    """
    keys_df = pl.DataFrame({"key": keys}).with_row_count("order")
    joined = keys_df.join(registry, on="key", how="left")
    missing = joined.filter(pl.col("latitud").is_null())
    if missing.height:
        missing_list = missing.select("key").to_series().to_list()
        raise KeyError(
            f"Keys not found: {missing_list[:10]}"
            + (" ..." if len(missing_list) > 10 else "")
        )
    return joined.sort("order").drop("order")
