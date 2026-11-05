# csvtool

Load a CSV, clean it with pandas, and print summary statistics.

## Install
```bash
pip install -e ".[dev]"
```

## Usage
```bash
csvtool data.csv
csvtool data.csv --clean --na mean --output cleaned.csv
csvtool data.csv --delimiter ";" --columns name,age
```

## Cleaning rules (`--clean`)
1. Normalize column names (lowercase, underscores)
2. Strip whitespace; blank strings become missing
3. Drop fully empty rows/columns
4. Drop duplicate rows
5. Convert numeric and ISO-8601 date columns
6. Handle missing values via `--na drop|mean|zero|keep`

## Development
```bash
pytest --cov=csvtool
ruff check . && mypy src
```