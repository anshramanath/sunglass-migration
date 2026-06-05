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

ATTR_OVERRIDES = {
    "monster": {
        "Cleaner Spray Bottle QTY":  "Quantity",
        "Qty":                       "Quantity",
        "Frame Styles for Filter":   "Style",
        "Special Size for Filter":   "Size",
    },
}

def sim_clean_attr_name(raw_name):
    override = ATTR_OVERRIDES.get(brand_key, {}).get(raw_name)
    if override:
        return override
    name = re.sub(r'(?i)\s+for\s+filter$', '', raw_name).strip()
    name = re.sub(r'(?i)^choose\s+', '', name).strip()
    name = re.sub(r'(?i)^filter\s+by\s+', '', name).strip()
    name = re.sub(r'\s*\(.*?\)', '', name).strip()
    return name


def extract_model(sku: str) -> str:
    chunk = sku.split("-")[0]
    upper = chunk.upper()

    # Wiley X: WX-MODELNAME-...
    if upper == "WX":
        parts = sku.split("-")
        return f"WX-{parts[1].upper()}" if len(parts) > 1 else upper

    # X-Loop: XLOOP-NNNN-...
    if upper == "XLOOP":
        parts = sku.split("-")
        return f"XLOOP-{parts[1].upper()}" if len(parts) > 1 else upper

    # X-Loop: XP8XHDnnnn-...
    if upper.startswith("XP8XHD"):
        digits = re.search(r'\d+$', chunk)
        return f"XP8XHD-{digits.group()}" if digits else upper

    # House SKU: strip leading C (combo prefix), find NNXnn model number
    normalized = re.sub(r'^C(?=[A-Z])', '', chunk)
    m = re.search(r'\d+[Xx]\d+', normalized)
    if m:
        return m.group(0).upper()

    # Fallback: normalized first chunk as family identifier
    return normalized.upper()


variation_errors = {}   # vid -> [msgs]
seen_ids         = set()


def err(vid, msg):
    variation_errors.setdefault(vid, []).append(msg)


def is_num(v):
    try:
        float(v)
        return True
    except (TypeError, ValueError):
        return False


# ── Pass 1: per-variation structural checks + Veeqo + model extraction ─────────

for entry in raw:
    product_id = entry.get("product_id")

    if not isinstance(product_id, (int, float)):
        continue
    if product_id not in known_product_ids:
        for v in entry.get("variations", []):
            err(v.get("id"), f"product_id={product_id} not in validate-products")

    for v in entry.get("variations", []):
        vid = v.get("id")

        if not isinstance(vid, (int, float)):
            err(vid, "id is not a number")
            continue
        if vid in seen_ids:
            err(vid, "id is not unique")
            continue
        seen_ids.add(vid)

        # Veeqo presence check
        sku = v.get("sku", "").strip()
        if not sku or sku not in veeqo_skus:
            err(vid, "not in Veeqo")

        if not isinstance(v.get("parent_id"), (int, float)):
            err(vid, "parent_id is not a number")
        elif v["parent_id"] != product_id:
            err(vid, f"parent_id={v['parent_id']} does not match product_id={product_id}")

        if not isinstance(v.get("name"), str) or not v["name"].strip():
            err(vid, "name is not a valid non-empty string")

        if v.get("type") != "variation":
            err(vid, f"type must be 'variation', got {v.get('type')!r}")

        if v.get("status") != "publish":
            err(vid, f"status must be 'publish', got {v.get('status')!r}")

        price = v.get("price")
        if not isinstance(price, str) or not price.strip():
            err(vid, "price is missing or empty")
        elif not is_num(price):
            err(vid, f"price is not a valid number: {price!r}")
        elif float(price) <= 0:
            err(vid, f"price must be greater than zero, got {price}")

        rp = v.get("regular_price")
        sp = v.get("sale_price")
        if rp not in (None, "") and not is_num(rp):
            err(vid, f"regular_price is not a valid number: {rp!r}")
        if sp not in (None, "") and not is_num(sp):
            err(vid, f"sale_price is not a valid number: {sp!r}")
        if rp not in (None, "") and sp not in (None, "") and is_num(rp) and is_num(sp):
            if float(sp) >= float(rp):
                err(vid, f"sale_price ({sp}) >= regular_price ({rp})")
        if not isinstance(v.get("on_sale"), bool):
            err(vid, f"on_sale must be a boolean, got {v.get('on_sale')!r}")
        else:
            if v["on_sale"] and sp in (None, ""):
                err(vid, "on_sale=True but no sale_price")
            if sp not in (None, "") and not v["on_sale"]:
                err(vid, "sale_price set but on_sale=False")
        if sp in (None, "") and rp not in (None, "") and is_num(price) and is_num(rp):
            if price != rp:
                err(vid, f"no sale_price but price ({price}) != regular_price ({rp})")

        sq = v.get("stock_quantity")
        if sq is not None and not isinstance(sq, (int, float)):
            err(vid, f"stock_quantity must be a number or null, got {sq!r}")
        ss = v.get("stock_status")
        if not ss:
            err(vid, "stock_status is missing")
        elif ss not in ("instock", "outofstock"):
            err(vid, f"stock_status must be 'instock' or 'outofstock', got {ss!r}")

        w = v.get("weight")
        if w not in (None, "") and not is_num(w):
            err(vid, f"weight is not a valid number: {w!r}")
        dims = v.get("dimensions") or {}
        for dim in ("length", "width", "height"):
            dv = dims.get(dim)
            if dv not in (None, "") and not is_num(dv):
                err(vid, f"dimensions.{dim} is not a valid number: {dv!r}")

        img = v.get("image")
        if img is not None:
            if not isinstance(img, dict) or not img.get("src"):
                err(vid, "image present but has no src")
            else:
                if not img["src"].startswith("http"):
                    err(vid, f"image.src is not a valid URL: {img['src']!r}")
                if not isinstance(img.get("name"), str) or not img["name"].strip():
                    err(vid, "image.name is not a valid non-empty string")

        for a in v.get("attributes", []):
            if not isinstance(a.get("name"), str) or not a["name"].strip():
                err(vid, f"attribute name is not a valid non-empty string: {a}")
            if not isinstance(a.get("option"), str) or not a["option"].strip():
                err(vid, f"attribute '{a.get('name')}' has empty option")
        cleaned = [sim_clean_attr_name(a["name"]) for a in v.get("attributes", []) if isinstance(a.get("name"), str)]
        seen_names, dupes = set(), set()
        for n in cleaned:
            if n in seen_names:
                dupes.add(n)
            seen_names.add(n)
        if dupes:
            err(vid, f"attribute name collision after cleaning: {sorted(dupes)}")



# ── Pass 2: model number consistency per product ───────────────────────────────

survivors_by_product = defaultdict(list)
for entry in raw:
    pid = entry.get("product_id")
    for v in entry.get("variations", []):
        vid = v.get("id")
        if vid in variation_errors:
            continue
        sku = v.get("sku", "").strip()
        survivors_by_product[pid].append((vid, sku, extract_model(sku)))

for pid, group in survivors_by_product.items():
    models = {model for _, _, model in group}
    if len(models) > 1:
        for vid, sku, model in group:
            err(vid, f"model number mismatch within product: {sorted(models)}")


# ── Outputs ───────────────────────────────────────────────────────────────────

valid = [
    {
        "product_id": e["product_id"],
        "variations": [
            v for v in e["variations"]
            if v["id"] not in variation_errors
        ],
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
