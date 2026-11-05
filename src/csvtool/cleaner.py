from __future__ import annotations

import re
from typing import Literal

import pandas as pd
from pandas.api.types import is_object_dtype, is_string_dtype

NaStrategy = Literal["drop", "mean", "zero", "keep"]


def _is_text(s: pd.Series) -> bool:  # type: ignore[type-arg]
    return bool(is_object_dtype(s) or is_string_dtype(s))


def _slug(name: object) -> str:
    return re.sub(r"[^0-9a-z]+", "_", str(name).strip().lower()).strip("_")


def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Lowercase column names and replace non-alphanumerics with underscores."""
    out = df.copy()
    out.columns = pd.Index([_slug(c) for c in out.columns])
    return out


def strip_strings(df: pd.DataFrame) -> pd.DataFrame:
    """Strip whitespace from text values; blank strings become missing."""
    out = df.copy()
    for col in out.columns:
        if _is_text(out[col]):
            out[col] = out[col].str.strip().replace("", pd.NA)
    return out


def drop_empty(df: pd.DataFrame) -> pd.DataFrame:
    """Drop rows and columns that are entirely missing."""
    return df.dropna(how="all").dropna(axis=1, how="all").reset_index(drop=True)


def drop_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    return df.drop_duplicates().reset_index(drop=True)


def coerce_types(df: pd.DataFrame) -> pd.DataFrame:
    """Convert text columns to numbers or ISO-8601 datetimes when every value fits."""
    out = df.copy()
    for col in out.columns:
        s = out[col]
        if not _is_text(s):
            continue
        non_null = s.dropna()
        if non_null.empty:
            continue
        numeric = pd.to_numeric(s, errors="coerce")
        if numeric.notna().sum() == len(non_null):
            out[col] = numeric
            continue
        dates = pd.to_datetime(s, errors="coerce", format="ISO8601")
        if dates.notna().sum() == len(non_null):
            out[col] = dates
    return out


def handle_missing(df: pd.DataFrame, strategy: NaStrategy) -> pd.DataFrame:
    if strategy == "keep":
        return df.copy()
    if strategy == "drop":
        return df.dropna().reset_index(drop=True)
    out = df.copy()
    num_cols = out.select_dtypes(include="number").columns
    if strategy == "mean":
        out[num_cols] = out[num_cols].fillna(out[num_cols].mean())
    elif strategy == "zero":
        out[num_cols] = out[num_cols].fillna(0)
    return out


def clean(df: pd.DataFrame, na_strategy: NaStrategy = "keep") -> pd.DataFrame:
    """Run the full cleaning pipeline. Never mutates the input."""
    df = normalize_columns(df)
    df = strip_strings(df)
    df = drop_empty(df)
    df = drop_duplicates(df)
    df = coerce_types(df)
    return handle_missing(df, na_strategy)