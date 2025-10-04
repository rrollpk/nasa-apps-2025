import argparse, asyncio
from pathlib import Path
from .registry import load_registry
from .keys import make_key
from .pipeline import fetch_for_keys, fetch_for_keys_batched
from .config import HW_PAST_DAYS, AQ_PAST_DAYS, AQ_FORECAST_DAYS


def main():
    p = argparse.ArgumentParser(
        description="Fetch Open-Meteo AQ + historical weather by municipality key"
    )
    p.add_argument("--registry", required=True)
    p.add_argument("--key", action="append", default=[])
    p.add_argument(
        "--from-triplet",
        nargs=3,
        action="append",
        metavar=("COMUNIDAD", "PROVINCIA", "POBLACION"),
    )
    p.add_argument("--batched", action="store_true")
    p.add_argument("--batch-size", type=int, default=400)
    p.add_argument("--sleep", type=float, default=0.2)

    # Weather History API Window
    p.add_argument("--start")
    p.add_argument("--end")
    p.add_argument("--days", type=int, default=HW_PAST_DAYS)

    # Air Quality API Window
    p.add_argument("--aq-past-days", type=int, default=AQ_PAST_DAYS)
    p.add_argument("--aq-forecast-days", type=int, default=AQ_FORECAST_DAYS)

    p.add_argument("--out", default="aq_results.json")
    args = p.parse_args()

    reg = load_registry(args.registry)

    keys = list(args.key)
    if args.from_triplet:
        for c, p, o in args.from_triplet:
            keys.append(make_key(c, p, o))
    if not keys:
        raise SystemExit("No keys provided. Use --key or --from-triplet.")

    kwargs = dict(
        start=args.start,
        end=args.end,
        days=args.days,
        aq_past_days=args.aq_past_days,
        aq_forecast_days=args.aq_forecast_days,
    )

    if args.batched:
        out = asyncio.run(
            fetch_for_keys_batched(
                reg,
                keys,
                batch_size=args.batch_size,
                inter_batch_sleep=args.sleep,
                **kwargs,
            )
        )
    else:
        out = asyncio.run(fetch_for_keys(reg, keys, **kwargs))

    Path(args.out).write_bytes(out)
    print(f"Wrote {args.out} ({len(keys)} keys)")


if __name__ == "__main__":
    main()
