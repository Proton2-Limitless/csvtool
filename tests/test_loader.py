from pathlib import Path

import pytest

from csvtool.errors import CsvToolError
from csvtool.loader import load_csv


def test_loads_valid_file(messy_csv: Path) -> None:
    assert load_csv(messy_csv).shape[0] == 5


def test_missing_file(tmp_path: Path) -> None:
    with pytest.raises(CsvToolError, match="not found"):
        load_csv(tmp_path / "nope.csv")


def test_empty_file(tmp_path: Path) -> None:
    p = tmp_path / "empty.csv"
    p.write_text("")
    with pytest.raises(CsvToolError, match="empty"):
        load_csv(p)


def test_custom_delimiter(tmp_path: Path) -> None:
    p = tmp_path / "semi.csv"
    p.write_text("a;b\n1;2\n")
    assert list(load_csv(p, ";").columns) == ["a", "b"]


def test_latin1_fallback(tmp_path: Path) -> None:
    p = tmp_path / "latin.csv"
    p.write_bytes(b"name,city\nJos\xe9,Lagos\n")
    assert load_csv(p).loc[0, "name"] == "José"