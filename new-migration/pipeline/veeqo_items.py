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

out_dir = data_dir / "veeqo-items"
out_dir.mkdir(parents=True, exist_ok=True)

flag_reasons = {}
clean_items  = []
flagged_items = []

for item in items:
    pid = item["id"]
    if item["type"] == "variable":
        absent = [
            v["sku"] for v in item.get("variations", [])
            if isinstance(v, dict) and v.get("sku") and v["sku"] not in veeqo_skus
        ]
        if absent:
            total = len([v for v in item.get("variations", []) if isinstance(v, dict)])
            flag_reasons[pid] = [f"{len(absent)}/{total} variation SKUs absent from Veeqo"]
            flagged_items.append(item)
        else:
            clean_items.append(item)
    else:
        sku = item.get("sku", "")
        if sku and sku not in veeqo_skus:
            flag_reasons[pid] = [f"SKU {sku!r} absent from Veeqo"]
            flagged_items.append(item)
        else:
            clean_items.append(item)

flagged_out = [{"reasons": flag_reasons[p["id"]], "product": p} for p in flagged_items]

(out_dir / "items.json").write_text(json.dumps(clean_items, indent=2, ensure_ascii=False))
(out_dir / "flagged.json").write_text(json.dumps(flagged_out, indent=2, ensure_ascii=False))

print(f"Veeqo items — {brand_name}")
print(f"  CSV: {csv_path.name}  ({len(veeqo_skus):,} SKUs)")
print(f"  Input:   {len(items)}")
print(f"  Passed:  {len(clean_items)}")
print(f"  Flagged: {len(flagged_items)}\n")

for item in flagged_items:
    pid = item["id"]
    name = item.get("name", "")[:40]
    for msg in flag_reasons.get(pid, []):
        print(f"  [FLAG] id={pid} | {name} | {msg}")

print(f"\nSaved → {out_dir / 'items.json'} ({len(clean_items)} items)")
print(f"Saved → {out_dir / 'flagged.json'} ({len(flagged_items)} flagged)")
