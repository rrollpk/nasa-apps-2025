import argparse, asyncio
from pathlib import Path
from .registry import load_registry
from .keys import make_key
from .pipeline import fetch_for_keys, fetch_for_keys_batched


def main():
    p = argparse.ArgumentParser(description="Fetch Open-Meteo AQ by municipality key")
    p.add_argument("--registry", required=True, help="Path to municipios.csv")
    p.add_argument(
        "--key",
        action="append",
        help="Key(s) comunidad|provincia|poblacion",
        default=[],
    )
    p.add_argument(
        "--from-triplet",
        nargs=3,
        action="append",
        metavar=("COMUNIDAD", "PROVINCIA", "POBLACION"),
        help="Alt: pass triplet(s)",
    )
    p.add_argument(
        "--batched",
        action="store_true",
        help="Use batched fetch (recommended for many keys)",
    )
    p.add_argument("--batch-size", type=int, default=400)
    p.add_argument("--sleep", type=float, default=0.2)
    p.add_argument("--out", default="aq_results.json")
    args = p.parse_args()

    reg = load_registry(args.registry)

    keys = list(args.key)
    if args.from_triplet:
        for c, p, o in args.from_triplet:
            keys.append(make_key(c, p, o))
    if not keys:
        raise SystemExit("No keys provided. Use --key or --from-triplet.")

    if args.batched:
        out = asyncio.run(
            fetch_for_keys_batched(
                reg, keys, batch_size=args.batch_size, inter_batch_sleep=args.sleep
            )
        )
    else:
        out = asyncio.run(fetch_for_keys(reg, keys))

    Path(args.out).write_bytes(out)
    print(f"Wrote {args.out} ({len(keys)} keys)")


if __name__ == "__main__":
    main()
