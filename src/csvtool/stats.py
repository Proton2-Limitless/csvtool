from __future__ import annotations

from typing import Any

import pandas as pd


def _num(x: Any) -> float | None:
    return None if pd.isna(x) else float(x)


def compute_stats(df: pd.DataFrame) -> dict[str, Any]:
    """Compute summary statistics as plain data (easy to test)."""
    numeric = df.select_dtypes(include="number")
    other = df.select_dtypes(exclude="number")
    return {
        "rows": int(df.shape[0]),
        "columns": int(df.shape[1]),
        "dtypes": {str(c): str(t) for c, t in df.dtypes.items()},
        "nulls": {str(c): int(n) for c, n in df.isna().sum().items()},
        "numeric": {
            str(c): {
                "mean": _num(numeric[c].mean()),
                "std": _num(numeric[c].std()),
                "min": _num(numeric[c].min()),
                "median": _num(numeric[c].median()),
                "max": _num(numeric[c].max()),
            }
            for c in numeric.columns
        },
        "top_values": {
            str(c): {str(k): int(v) for k, v in other[c].value_counts().head(3).items()}
            for c in other.columns
        },
    }


def _fmt(x: float | None) -> str:
    return "-" if x is None else f"{x:.2f}"


def format_stats(stats: dict[str, Any]) -> str:
    """Render stats from compute_stats as terminal-friendly text."""
    lines = [f"Rows: {stats['rows']}", f"Columns: {stats['columns']}", ""]
    lines.append(f"{'Column':<20}{'Type':<18}{'Nulls':>6}")
    for col, dtype in stats["dtypes"].items():
        lines.append(f"{col:<20}{dtype:<18}{stats['nulls'][col]:>6}")
    if stats["numeric"]:
        lines += ["", "Numeric summary:"]
        lines.append(f"{'Column':<20}{'mean':>10}{'std':>10}{'min':>10}{'median':>10}{'max':>10}")
        for col, s in stats["numeric"].items():
            lines.append(
                f"{col:<20}{_fmt(s['mean']):>10}{_fmt(s['std']):>10}"
                f"{_fmt(s['min']):>10}{_fmt(s['median']):>10}{_fmt(s['max']):>10}"
            )
    if stats["top_values"]:
        lines += ["", "Top values:"]
        for col, counts in stats["top_values"].items():
            pairs = ", ".join(f"{k} ({v})" for k, v in counts.items())
            lines.append(f"  {col}: {pairs or '-'}")
    return "\n".join(lines)