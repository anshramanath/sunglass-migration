import csv
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from config import BASE, load_brand


brand_key, config = load_brand()
slug       = config["slug"]
brand_name = config["brand_name"]

products_path   = BASE / "data" / slug / "validate-products" / "products.json"
variations_path = BASE / "data" / slug / "slim-variations" / "variations.json"

if not products_path.exists():
    raise SystemExit(f"Run validate_products.py first. Not found: {products_path}")
if not variations_path.exists():
    raise SystemExit(f"Run slim_variations.py first. Not found: {variations_path}")

csv_candidates = sorted((BASE.parent).glob("sellables_export*.csv"))
if not csv_candidates:
    raise SystemExit(f"No sellables_export*.csv found in {BASE.parent}")

veeqo_skus = set()
with open(csv_candidates[0], newline="", encoding="utf-8-sig") as f:
    for row in csv.DictReader(f):
        sku = row.get("sku_code", "").strip()
        if sku:
            veeqo_skus.add(sku)

products = json.loads(products_path.read_text())
raw      = json.loads(variations_path.read_text())

known_product_ids = {p["id"] for p in products}

out_dir = BASE / "data" / slug / "validate-variations"
out_dir.mkdir(parents=True, exist_ok=True)


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


variation_errors = {}
seen_ids         = set()


def err(vid, msg):
    variation_errors.setdefault(vid, []).append(msg)


# ── Pass 1: Veeqo ─────────────────────────────────────────────────────────────

for entry in raw:
    product_id = entry.get("product_id")
    if product_id not in known_product_ids:
        continue

    for v in entry.get("variations", []):
        vid = v.get("id")

        if vid in seen_ids:
            err(vid, "id is not unique")
            continue
        seen_ids.add(vid)

        sku = v.get("sku", "").strip()
        if not sku or sku not in veeqo_skus:
            err(vid, "not in Veeqo")

        seen_attr_names = {}
        for a in v.get("attributes", []):
            raw     = a.get("name", "")
            cleaned = clean_attr_name(raw)
            if cleaned in seen_attr_names:
                err(vid, f"attribute name collision: '{seen_attr_names[cleaned]}' and '{raw}' both clean to '{cleaned}'")
            else:
                seen_attr_names[cleaned] = raw


# ── Pass 2: model presence + consistency ──────────────────────────────────────

model_groups = defaultdict(list)  # pid -> [(vid, sku, model), ...]

for entry in raw:
    pid = entry.get("product_id")
    for v in entry.get("variations", []):
        vid = v.get("id")
        if vid in variation_errors:
            continue
        sku   = v.get("sku", "").strip()
        model = extract_model(sku)
        if model is None:
            err(vid, "SKU has no recognizable model number")
        else:
            model_groups[pid].append((vid, sku, model))

for pid, group in model_groups.items():
    models = {model for _, _, model in group}
    if len(models) > 1:
        for vid, sku, model in group:
            err(vid, f"model number mismatch within product: {sorted(models)}")


# ── Outputs ───────────────────────────────────────────────────────────────────

valid = [
    {
        "product_id": e["product_id"],
        "variations": [v for v in e["variations"] if v["id"] not in variation_errors],
    }
    for e in raw
]
valid = [e for e in valid if e["variations"]]

flagged = [
    {"reasons": variation_errors[v["id"]], "variation": v}
    for entry in raw for v in entry["variations"]
    if v["id"] in variation_errors
]

(out_dir / "variations.json").write_text(json.dumps(valid, indent=2, ensure_ascii=False))
(out_dir / "flagged.json").write_text(json.dumps(flagged, indent=2, ensure_ascii=False))

total_in      = sum(len(e["variations"]) for e in raw)
total_out     = sum(len(e["variations"]) for e in valid)
total_flagged = len(flagged)

print(f"Brand: {brand_name} ({slug})")
print(f"Veeqo CSV: {csv_candidates[0].name}  ({len(veeqo_skus):,} SKUs)\n")
print(f"Validated {total_in:,} variations\n")
print(f"  Passed:  {total_out:,}")
print(f"  Flagged: {total_flagged:,}\n")

for entry in raw:
    for v in entry["variations"]:
        vid = v["id"]
        for msg in variation_errors.get(vid, []):
            print(f"  [FLAG] id={vid} | parent={v.get('parent_id')} | {v.get('sku', '')} | {msg}")

print(f"\nSaved → {out_dir / 'variations.json'} ({total_out:,} variations)")
print(f"Saved → {out_dir / 'flagged.json'} ({total_flagged:,} flagged)")
