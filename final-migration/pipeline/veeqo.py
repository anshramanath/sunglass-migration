import csv
from pathlib import Path

_csv = sorted(Path(__file__).parent.glob("sellables_export*.csv"))
if not _csv:
    raise SystemExit("No sellables_export*.csv found in pipeline/")

_skus = set()
with open(_csv[0], newline="", encoding="utf-8-sig") as f:
    for row in csv.DictReader(f):
        sku = row.get("sku_code", "").strip()
        if sku:
            _skus.add(sku)

def check_veeqo(sku: str) -> bool:
    return sku in _skus
