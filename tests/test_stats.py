import pandas as pd

from csvtool.stats import compute_stats, format_stats


def test_compute_stats_basic() -> None:
    df = pd.DataFrame({"a": [1, 2, 3], "b": ["x", "x", "y"]})
    s = compute_stats(df)
    assert (s["rows"], s["columns"]) == (3, 2)
    assert s["numeric"]["a"]["mean"] == 2.0
    assert s["top_values"]["b"] == {"x": 2, "y": 1}


def test_all_null_numeric_column() -> None:
    df = pd.DataFrame({"a": [None, None]}, dtype="float64")
    s = compute_stats(df)
    assert s["nulls"]["a"] == 2
    assert s["numeric"]["a"]["mean"] is None


def test_format_stats_contains_key_info() -> None:
    text = format_stats(compute_stats(pd.DataFrame({"a": [1, 2], "b": ["x", "y"]})))
    assert "Rows: 2" in text
    assert "Numeric summary" in text
    assert "Top values" in text