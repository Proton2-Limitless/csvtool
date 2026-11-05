from __future__ import annotations

import argparse
import sys
from collections.abc import Sequence
from pathlib import Path

from . import __version__
from .cleaner import clean
from .errors import CsvToolError
from .loader import load_csv
from .stats import compute_stats, format_stats


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="csvtool", description="Load, clean and summarize a CSV file."
    )
    p.add_argument("path", type=Path, help="path to the CSV file")
    p.add_argument("--clean", action="store_true", help="apply cleaning pipeline")
    p.add_argument(
        "--na",
        choices=["drop", "mean", "zero", "keep"],
        default="keep",
        help="missing-value strategy, used with --clean (default: keep)",
    )
    p.add_argument("--columns", help="comma-separated columns to keep")
    p.add_argument("--delimiter", default=",", help="field delimiter (default: ,)")
    p.add_argument("--output", type=Path, help="write resulting data to this CSV")
    p.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    return p


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        df = load_csv(args.path, args.delimiter)
        if args.clean:
            df = clean(df, args.na)
        if args.columns:
            wanted = [c.strip() for c in args.columns.split(",")]
            missing = [c for c in wanted if c not in df.columns]
            if missing:
                raise CsvToolError(f"Unknown column(s): {', '.join(missing)}")
            df = df[wanted]
        print(format_stats(compute_stats(df)))
        if args.output:
            df.to_csv(args.output, index=False)
            print(f"\nWrote {args.output}")
    except CsvToolError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())