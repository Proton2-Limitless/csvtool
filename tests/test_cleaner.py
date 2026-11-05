import pandas as pd
import pytest

from csvtool.cleaner import (
    NaStrategy,
    clean,
    coerce_types,
    drop_duplicates,
    drop_empty,
    normalize_columns,
    strip_strings,
)


def test_normalize_columns() -> None:
    df = pd.DataFrame(columns=[" Signup Date ", "Age (yrs)"])
    assert list(normalize_columns(df).columns) == ["signup_date", "age_yrs"]


def test_strip_strings_and_blank_to_na() -> None:
    df = pd.DataFrame({"a": ["  x ", "   "]})
    out = strip_strings(df)
    assert out.loc[0, "a"] == "x"
    assert pd.isna(out.loc[1, "a"])


def test_drop_empty() -> None:
    df = pd.DataFrame({"a": [1, None], "b": [None, None]})
    out = drop_empty(df)
    assert out.shape == (1, 1)


def test_drop_duplicates() -> None:
    df = pd.DataFrame({"a": [1, 1, 2]})
    assert len(drop_duplicates(df)) == 2


def test_coerce_types() -> None:
    df = pd.DataFrame(
        {"n": ["1", "2.5", None], "d": ["2024-01-01", "2024-02-01", None], "s": ["a", "b", "c"]}
    )
    out = coerce_types(df)
    assert pd.api.types.is_numeric_dtype(out["n"])
    assert pd.api.types.is_datetime64_any_dtype(out["d"])
    assert not pd.api.types.is_numeric_dtype(out["s"])


@pytest.mark.parametrize(
    ("strategy", "expected_rows", "expected_age"),
    [("keep", 3, None), ("drop", 2, None), ("mean", 3, 35.5), ("zero", 3, 0.0)],
)
def test_na_strategies(
    messy_df: pd.DataFrame,
    strategy: NaStrategy,
    expected_rows: int,
    expected_age: float | None,
) -> None:
    out = clean(messy_df, strategy)
    assert len(out) == expected_rows
    if expected_age is not None:
        bob = out[out["name"] == "Bob"].iloc[0]
        assert bob["age"] == expected_age


def test_clean_does_not_mutate_input(messy_df: pd.DataFrame) -> None:
    before = messy_df.copy()
    clean(messy_df, "drop")
    pd.testing.assert_frame_equal(messy_df, before)