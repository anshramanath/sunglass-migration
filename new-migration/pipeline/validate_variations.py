import json
import os
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from config import BASE, load_brand


brand_key, config = load_brand()
slug       = config["slug"]
brand_name = config["brand_name"]

products_path = BASE / "data" / slug / "validate-products" / "products.json"
variations_path = BASE / "data" / slug / "slim-variations" / "variations.json"

if not products_path.exists():
    raise SystemExit(f"Run validate_products.py first. Not found: {products_path}")
if not variations_path.exists():
    raise SystemExit(f"Run slim_variations.py first. Not found: {variations_path}")

products = json.loads(products_path.read_text())
raw = json.loads(variations_path.read_text())

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

def sim_clean_attr_name(raw):
    override = ATTR_OVERRIDES.get(brand_key, {}).get(raw)
    if override:
        return override
    name = re.sub(r'(?i)\s+for\s+filter$', '', raw).strip()
    name = re.sub(r'(?i)^choose\s+', '', name).strip()
    name = re.sub(r'(?i)^filter\s+by\s+', '', name).strip()
    name = re.sub(r'\s*\(.*?\)', '', name).strip()
    return name

variation_errors = {}  # vid -> [msgs]
seen_ids = set()
seen_skus = {}  # sku -> vid

def err(vid, msg):
    variation_errors.setdefault(vid, []).append(msg)

def is_num(v):
    try:
        float(v)
        return True
    except (TypeError, ValueError):
        return False

for entry in raw:
    product_id = entry.get("product_id")

    # product_id: number, known
    if not isinstance(product_id, (int, float)):
        # can't proceed without a valid product_id — skip entry
        continue
    if product_id not in known_product_ids:
        # flag all variations in this entry
        for v in entry.get("variations", []):
            err(v.get("id"), f"product_id={product_id} not in validate-products")

    for v in entry.get("variations", []):
        vid = v.get("id")

        # id: number, unique
        if not isinstance(vid, (int, float)):
            err(vid, "id is not a number")
        elif vid in seen_ids:
            err(vid, "id is not unique")
        else:
            seen_ids.add(vid)

        # parent_id: number, matches entry product_id
        if not isinstance(v.get("parent_id"), (int, float)):
            err(vid, "parent_id is not a number")
        elif v["parent_id"] != product_id:
            err(vid, f"parent_id={v['parent_id']} does not match product_id={product_id}")

        # name: non-empty string
        if not isinstance(v.get("name"), str) or not v["name"].strip():
            err(vid, "name is not a valid non-empty string")

        # type: must be "variation"
        if v.get("type") != "variation":
            err(vid, f"type must be 'variation', got {v.get('type')!r}")

        # status: must be "publish"
        if v.get("status") != "publish":
            err(vid, f"status must be 'publish', got {v.get('status')!r}")

        # description: string or null
        if v.get("description") is not None and not isinstance(v["description"], str):
            err(vid, "description must be a string or null")

        # permalink: non-empty string
        if not isinstance(v.get("permalink"), str) or not v["permalink"].strip():
            err(vid, "permalink is not a valid non-empty string")

        # sku: non-empty string, no spaces, unique
        sku = v.get("sku")
        if not isinstance(sku, str) or not sku.strip():
            err(vid, "sku is not a valid non-empty string")
        elif " " in sku:
            err(vid, f"sku contains spaces: {sku!r}")
        elif sku in seen_skus:
            err(vid, f"duplicate sku {sku!r} already seen on id={seen_skus[sku]}")
        else:
            seen_skus[sku] = vid

        # price: required, valid number greater than zero
        price = v.get("price")
        if not isinstance(price, str) or not price.strip():
            err(vid, "price is missing or empty")
        elif not is_num(price):
            err(vid, f"price is not a valid number: {price!r}")
        elif float(price) <= 0:
            err(vid, f"price must be greater than zero, got {price}")

        # regular_price: null or empty OK; if present must be valid number
        rp = v.get("regular_price")
        if rp not in (None, "") and not is_num(rp):
            err(vid, f"regular_price is not a valid number: {rp!r}")

        # sale_price: null or empty OK; if present must be valid number < regular_price
        sp = v.get("sale_price")
        if sp not in (None, "") and not is_num(sp):
            err(vid, f"sale_price is not a valid number: {sp!r}")
        if rp not in (None, "") and sp not in (None, ""):
            if float(sp) >= float(rp):
                err(vid, f"sale_price ({sp}) >= regular_price ({rp})")

        # on_sale: boolean + consistency with sale_price
        if not isinstance(v.get("on_sale"), bool):
            err(vid, f"on_sale must be a boolean, got {v.get('on_sale')!r}")
        else:
            if v["on_sale"] and sp in (None, ""):
                err(vid, "on_sale=True but no sale_price")
            if sp not in (None, "") and not v["on_sale"]:
                err(vid, "sale_price set but on_sale=False")

        # when no sale_price: price must equal regular_price
        if sp in (None, "") and rp not in (None, "") and is_num(price) and is_num(rp):
            if price != rp:
                err(vid, f"no sale_price but price ({price}) != regular_price ({rp})")

        # stock_quantity: number or null
        sq = v.get("stock_quantity")
        if sq is not None and not isinstance(sq, (int, float)):
            err(vid, f"stock_quantity must be a number or null, got {sq!r}")

        # stock_status: required, instock or outofstock
        ss = v.get("stock_status")
        if not ss:
            err(vid, "stock_status is missing")
        elif ss not in ("instock", "outofstock"):
            err(vid, f"stock_status must be 'instock' or 'outofstock', got {ss!r}")

        # weight: null or empty OK; if present must be valid number
        w = v.get("weight")
        if w not in (None, "") and not is_num(w):
            err(vid, f"weight is not a valid number: {w!r}")

        # dimensions: each subfield null/empty or valid number
        dims = v.get("dimensions") or {}
        for dim in ("length", "width", "height"):
            dv = dims.get(dim)
            if dv not in (None, "") and not is_num(dv):
                err(vid, f"dimensions.{dim} is not a valid number: {dv!r}")

        # image: src starts with http, name non-empty string
        img = v.get("image")
        if not isinstance(img, dict) or not img.get("src"):
            err(vid, "image is missing or has no src")
        else:
            if not img["src"].startswith("http"):
                err(vid, f"image.src is not a valid URL: {img['src']!r}")
            if not isinstance(img.get("name"), str) or not img["name"].strip():
                err(vid, "image.name is not a valid non-empty string")

        # attributes: each has non-empty name and option
        for a in v.get("attributes", []):
            if not isinstance(a.get("name"), str) or not a["name"].strip():
                err(vid, f"attribute name is not a valid non-empty string: {a}")
            if not isinstance(a.get("option"), str) or not a["option"].strip():
                err(vid, f"attribute '{a.get('name')}' has empty option")
        # attribute name collision check
        cleaned = [sim_clean_attr_name(a["name"]) for a in v.get("attributes", []) if isinstance(a.get("name"), str)]
        seen, dupes = set(), set()
        for n in cleaned:
            if n in seen:
                dupes.add(n)
            seen.add(n)
        if dupes:
            err(vid, f"attribute name collision after cleaning: {sorted(dupes)}")

    # base SKU consistency: all variations in a product must share the same pre-dash base
    valid_sku_vars = [(v["id"], v["sku"]) for v in entry.get("variations", [])
                     if isinstance(v.get("sku"), str) and v["sku"].strip() and " " not in v["sku"]]
    if valid_sku_vars:
        bases = {sku.split("-")[0] for _, sku in valid_sku_vars}
        if len(bases) > 1:
            for v in entry.get("variations", []):
                err(v["id"], f"sku base mismatch: product has mixed pre-dash bases {sorted(bases)}")

# ── Outputs ───────────────────────────────────────────────────────────────────
all_variation_ids = {v["id"] for entry in raw for v in entry["variations"]}

valid = [
    {"product_id": e["product_id"], "variations": [v for v in e["variations"] if v["id"] not in variation_errors]}
    for e in raw
]
# drop entries where all variations were flagged
valid = [e for e in valid if e["variations"]]

flagged = [
    {"reasons": variation_errors[v["id"]], "variation": v}
    for entry in raw for v in entry["variations"]
    if v["id"] in variation_errors
]

(out_dir / "variations.json").write_text(json.dumps(valid, indent=2, ensure_ascii=False))
(out_dir / "flagged.json").write_text(json.dumps(flagged, indent=2, ensure_ascii=False))

# ── Console summary ───────────────────────────────────────────────────────────
total_in  = sum(len(e["variations"]) for e in raw)
total_out = sum(len(e["variations"]) for e in valid)
total_issues = sum(len(v) for v in variation_errors.values())

print(f"Validated {total_in} variations\n")
print(f"  Passed:  {total_out}")
print(f"  Flagged: {len(flagged)}  ({total_issues} issues)\n")

for entry in raw:
    for v in entry["variations"]:
        vid = v["id"]
        for msg in variation_errors.get(vid, []):
            print(f"  [ERROR] id={vid} | parent={v.get('parent_id')} | {v.get('sku', '')} | {msg}")

print(f"\nSaved → {out_dir / 'variations.json'} ({total_out} variations)")
print(f"Saved → {out_dir / 'flagged.json'} ({len(flagged)} flagged)")

if not variation_errors:
    print(f"\n  → Next: python pipeline/reshape_items.py")
