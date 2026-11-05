from pathlib import Path

import pandas as pd
import pytest

MESSY = """ Name , Age ,City,Signup Date
 Alice ,30,Lagos,2024-01-05
Bob,,Abuja,2024-02-10
Alice ,30,Lagos,2024-01-05
,,,
Carol,41, Kano ,2024-03-15
"""


@pytest.fixture
def messy_csv(tmp_path: Path) -> Path:
    p = tmp_path / "messy.csv"
    p.write_text(MESSY, encoding="utf-8")
    return p


@pytest.fixture
def messy_df(messy_csv: Path) -> pd.DataFrame:
    return pd.read_csv(messy_csv)