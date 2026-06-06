import csv
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from config import BASE, load_brand


brand_key, config = load_brand()
slug       = config["slug"]
brand_name = config["brand_name"]

data = json.loads((BASE / "data" / slug / "slim-products" / "products.json").read_text())

csv_candidates = sorted((BASE.parent).glob("sellables_export*.csv"))
if not csv_candidates:
    raise SystemExit(f"No sellables_export*.csv found in {BASE.parent}")

veeqo_skus = set()
with open(csv_candidates[0], newline="", encoding="utf-8-sig") as f:
    for row in csv.DictReader(f):
        sku = row.get("sku_code", "").strip()
        if sku:
            veeqo_skus.add(sku)

out_dir = BASE / "data" / slug / "validate-products"
out_dir.mkdir(parents=True, exist_ok=True)

product_errors = {}

def err(pid, msg):
    product_errors.setdefault(pid, []).append(msg)

def clean_attr_name(raw):
    name = re.sub(r'(?i)\s+for\s+filter$', '', raw).strip()
    name = re.sub(r'(?i)^choose\s+', '', name).strip()
    name = re.sub(r'(?i)^filter\s+by\s+', '', name).strip()
    name = re.sub(r'\s*\(.*?\)', '', name).strip()
    return name

def extract_model(sku: str):
    """Return the digits-X-digits model number from the first SKU segment, or None."""
    chunk      = sku.split("-")[0]
    normalized = re.sub(r'^C(?=[A-Z])', '', chunk)  # strip leading C combo prefix
    m = re.search(r'\d+[Xx]\d+', normalized)
    return m.group(0).upper() if m else None

for p in data:
    pid        = p.get("id")
    is_variable = bool(p.get("variations"))

    # Simple products: must be in Veeqo and have a recognizable model number
    if not is_variable:
        sku = p.get("sku", "").strip()
        if not sku or sku not in veeqo_skus:
            err(pid, "not in Veeqo")
        if not sku or extract_model(sku) is None:
            err(pid, "SKU has no recognizable model number")

    # Attribute name collision check (all products)
    seen_attr_names = {}
    for a in p.get("attributes", []):
        raw     = a.get("name", "")
        cleaned = clean_attr_name(raw)
        if cleaned in seen_attr_names:
            err(pid, f"attribute name collision: '{seen_attr_names[cleaned]}' and '{raw}' both clean to '{cleaned}'")
        else:
            seen_attr_names[cleaned] = raw


# ── Outputs ───────────────────────────────────────────────────────────────────
valid   = [p for p in data if p["id"] not in product_errors]
flagged = [
    {"reasons": product_errors[p["id"]], "product": p}
    for p in data if p["id"] in product_errors
]

with open(out_dir / "products.json", "w", encoding="utf-8") as f:
    json.dump(valid, f, indent=2, ensure_ascii=False)
with open(out_dir / "flagged.json", "w", encoding="utf-8") as f:
    json.dump(flagged, f, indent=2, ensure_ascii=False)

total_issues = sum(len(v) for v in product_errors.values())
print(f"Brand: {brand_name} ({slug})")
print(f"Veeqo CSV: {csv_candidates[0].name}  ({len(veeqo_skus):,} SKUs)\n")
print(f"Validated {len(data)} products\n")
print(f"  Passed:  {len(valid)}")
print(f"  Flagged: {len(flagged)}  ({total_issues} issues)\n")

for p in data:
    pid  = p["id"]
    name = (p.get("name") or "")[:45]
    for e in product_errors.get(pid, []):
        print(f"  [FLAG] id={pid} | {name} | {e}")

print(f"\nSaved → {out_dir / 'products.json'} ({len(valid)} products)")
print(f"Saved → {out_dir / 'flagged.json'} ({len(flagged)} flagged)")
