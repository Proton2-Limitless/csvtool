from __future__ import annotations

from pathlib import Path

import pandas as pd

from .errors import CsvToolError


def _read(path: Path, delimiter: str, encoding: str) -> pd.DataFrame:
    return pd.read_csv(path, sep=delimiter, encoding=encoding)


def load_csv(path: Path, delimiter: str = ",") -> pd.DataFrame:
    """Load a CSV file, trying UTF-8 first and falling back to latin-1."""
    if not path.is_file():
        raise CsvToolError(f"File not found: {path}")
    try:
        try:
            return _read(path, delimiter, "utf-8")
        except UnicodeDecodeError:
            return _read(path, delimiter, "latin-1")
    except pd.errors.EmptyDataError as exc:
        raise CsvToolError(f"File is empty: {path}") from exc
    except pd.errors.ParserError as exc:
        raise CsvToolError(f"Could not parse {path}: {exc}") from exc