from pathlib import Path

import pytest

from csvtool.cli import main


def test_prints_stats(messy_csv: Path, capsys: pytest.CaptureFixture[str]) -> None:
    assert main([str(messy_csv)]) == 0
    assert "Rows: 5" in capsys.readouterr().out


def test_clean_flag(messy_csv: Path, capsys: pytest.CaptureFixture[str]) -> None:
    assert main([str(messy_csv), "--clean", "--na", "drop"]) == 0
    assert "Rows: 2" in capsys.readouterr().out


def test_output_file(messy_csv: Path, tmp_path: Path) -> None:
    out = tmp_path / "out.csv"
    assert main([str(messy_csv), "--clean", "--output", str(out)]) == 0
    assert out.exists()
    assert out.read_text().startswith("name,age,city,signup_date")


def test_missing_file(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    assert main([str(tmp_path / "nope.csv")]) == 1
    assert "error:" in capsys.readouterr().err


def test_unknown_column(messy_csv: Path, capsys: pytest.CaptureFixture[str]) -> None:
    assert main([str(messy_csv), "--clean", "--columns", "bogus"]) == 1
    assert "Unknown column" in capsys.readouterr().err


def test_version(capsys: pytest.CaptureFixture[str]) -> None:
    with pytest.raises(SystemExit) as exc:
        main(["--version"])
    assert exc.value.code == 0