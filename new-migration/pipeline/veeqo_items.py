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

item_errors = {}

def flag(pid, msg):
    item_errors.setdefault(pid, []).append(msg)

for item in items:
    pid = item["id"]

    if item["type"] == "variable":
        for v in item.get("variations", []):
            if isinstance(v, dict) and v.get("sku") and v["sku"] not in veeqo_skus:
                flag(pid, f"variation {v['id']} sku not in Veeqo: {v['sku']!r}")
    else:
        sku = item.get("sku", "")
        if sku and sku not in veeqo_skus:
            flag(pid, f"sku not in Veeqo: {sku!r}")

flagged_ids = set(item_errors)
valid   = [p for p in items if p["id"] not in flagged_ids]
flagged = [{"reasons": item_errors[p["id"]], "product": p} for p in items if p["id"] in flagged_ids]

(out_dir / "items.json").write_text(json.dumps(valid, indent=2, ensure_ascii=False))
(out_dir / "flagged.json").write_text(json.dumps(flagged, indent=2, ensure_ascii=False))

total_vars   = sum(len([v for v in p.get("variations", []) if isinstance(v, dict)]) for p in valid)
total_issues = sum(len(v) for v in item_errors.values())

print(f"Veeqo check — {brand_name}")
print(f"  CSV: {csv_path.name}  ({len(veeqo_skus):,} SKUs)")
print()
print(f"  Passed:  {len(valid)}  ({total_vars} variations)")
print(f"  Flagged: {len(flagged)}  ({total_issues} issues)")

if flagged:
    print()
    for entry in flagged:
        p = entry["product"]
        print(f"  [FLAG] id={p['id']} | {p.get('name', '')[:50]}")
        for r in entry["reasons"][:5]:
            print(f"           {r}")
        if len(entry["reasons"]) > 5:
            print(f"           ... and {len(entry['reasons']) - 5} more")

print(f"\nSaved → {out_dir / 'items.json'} ({len(valid)} items)")
print(f"Saved → {out_dir / 'flagged.json'} ({len(flagged)} flagged)")
print(f"\n  → Next: python pipeline/{slug}_categorize_items.py")
