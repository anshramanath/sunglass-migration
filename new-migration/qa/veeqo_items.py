import csv
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from config import BASE, load_brand


brand_key, config = load_brand()
slug       = config["slug"]
brand_name = config["brand_name"]
data_dir = BASE / "data" / slug

items_path = data_dir / "create-items" / "items.json"
if not items_path.exists():
    raise SystemExit(f"Run create_items.py first. Not found: {items_path}")

csv_candidates = sorted((BASE.parent).glob("sellables_export*.csv"))
if not csv_candidates:
    raise SystemExit(f"No sellables_export*.csv found in {BASE.parent}")
csv_path = csv_candidates[0]

veeqo_skus = set()
with open(csv_path, newline="", encoding="utf-8-sig") as f:
    for row in csv.DictReader(f):
        sku = row.get("sku_code", "").strip()
        if sku:
            veeqo_skus.add(sku)

items = json.loads(items_path.read_text())

missing = []
for item in items:
    if item["type"] == "variable":
        absent = [v["sku"] for v in item.get("variations", [])
                  if isinstance(v, dict) and v.get("sku") and v["sku"] not in veeqo_skus]
        if absent:
            total = len([v for v in item.get("variations", []) if isinstance(v, dict)])
            missing.append({"id": item["id"], "name": item.get("name", ""), "absent": absent, "total": total})
    else:
        sku = item.get("sku", "")
        if sku and sku not in veeqo_skus:
            missing.append({"id": item["id"], "name": item.get("name", ""), "absent": [sku], "total": 1})

print(f"Veeqo SKU check — {brand_name}")
print(f"  CSV: {csv_path.name}  ({len(veeqo_skus):,} SKUs)")
print(f"  Items checked: {len(items)}")
print(f"  Not in Veeqo:  {len(missing)}")

if missing:
    print()
    for entry in missing:
        print(f"  id={entry['id']} | {entry['name'][:50]}")
        print(f"    {len(entry['absent'])}/{entry['total']} SKUs absent")
        for sku in entry["absent"][:3]:
            print(f"      {sku}")
        if len(entry["absent"]) > 3:
            print(f"      ... and {len(entry['absent']) - 3} more")
