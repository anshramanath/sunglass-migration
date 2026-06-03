import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from config import BASE, load_brand


brand_key, config = load_brand()
slug       = config["slug"]
brand_name = config["brand_name"]
data_dir = BASE / "data" / slug

items          = json.loads((data_dir / "create-items"     / "items.json").read_text())
flagged_out    = json.loads((data_dir / "create-items"     / "flagged.json").read_text())
source_products = json.loads((data_dir / "reshape-products" / "products.json").read_text())
source_vars_raw = json.loads((data_dir / "reshape-variations" / "variations.json").read_text())

source_by_id   = {p["id"]: p for p in source_products}
vars_by_product = {e["product_id"]: {v["id"]: v for v in e["variations"]} for e in source_vars_raw}

errors = []

def err(pid, msg):
    errors.append(f"id={pid} | {msg}")

# ── Coverage ──────────────────────────────────────────────────────────────────
item_ids    = {p["id"] for p in items}
flagged_ids = {e["product"]["id"] for e in flagged_out}
source_ids  = {p["id"] for p in source_products}

for pid in source_ids - item_ids - flagged_ids:
    err(pid, "product missing from both items.json and flagged.json")
for pid in item_ids & flagged_ids:
    err(pid, "product appears in both items.json and flagged.json")

# ── Per-item checks ───────────────────────────────────────────────────────────
seen_var_ids = {}   # variation_id -> product_id
seen_skus    = {}   # sku -> product_id

for item in items:
    pid = item["id"]
    s   = source_by_id.get(pid)
    if s is None:
        err(pid, "item not found in reshape-products source")
        continue

    is_variable = item["type"] == "variable"
    variations  = item.get("variations", [])

    # no ints left in variations
    ints = [v for v in variations if isinstance(v, int)]
    if ints:
        err(pid, f"variations[] still contains unreplaced IDs: {ints}")

    if is_variable:
        source_var_ids = set(s.get("variations", []))
        s_vars         = vars_by_product.get(pid, {})

        for v in [x for x in variations if isinstance(x, dict)]:
            vid = v["id"]

            # variation id was in product's original list
            if vid not in source_var_ids:
                err(pid, f"embedded variation {vid} was not in source product's variations[]")

            # parent_id matches
            if v.get("parent_id") != pid:
                err(pid, f"variation {vid} parent_id={v.get('parent_id')} != product id={pid}")

            # variation exists in reshape-variations for this product
            if vid not in s_vars:
                err(pid, f"variation {vid} not found in reshape-variations for this product")

            # image dedup: no variation image should duplicate a parent image
            parent_srcs = {img["src"] for img in item.get("images", [])}
            for vimg in v.get("images", []):
                if vimg["src"] in parent_srcs:
                    err(pid, f"variation {vid} images[] contains src duplicating parent image: {vimg['src']}")

            # variation attributes exist in product attribute pool
            product_attr_map = {a["name"]: set(a["options"]) for a in item.get("attributes", [])}
            for a in v.get("attributes", []):
                if a["name"] not in product_attr_map:
                    err(pid, f"variation {vid} attribute '{a['name']}' not in product attributes")
                elif a["option"] not in product_attr_map[a["name"]]:
                    err(pid, f"variation {vid} attribute '{a['name']}'='{a['option']}' not in product options")

            # global variation ID uniqueness
            if vid in seen_var_ids:
                err(pid, f"variation id={vid} also on product id={seen_var_ids[vid]}")
            else:
                seen_var_ids[vid] = pid

        # min/max price matches variation data
        filled = [v for v in variations if isinstance(v, dict)]
        if filled:
            reg_prices = [v["regularPriceCents"] for v in filled if v.get("regularPriceCents") is not None]
            if reg_prices:
                if item.get("minPriceCents") != min(reg_prices):
                    err(pid, f"minPriceCents={item.get('minPriceCents')} expected {min(reg_prices)}")
                if item.get("maxPriceCents") != max(reg_prices):
                    err(pid, f"maxPriceCents={item.get('maxPriceCents')} expected {max(reg_prices)}")
            computed_sale = any(v.get("sale") for v in filled)
            if item.get("sale") != computed_sale:
                err(pid, f"sale={item.get('sale')} expected {computed_sale}")
    else:
        # simple: variations must be empty
        if variations:
            err(pid, f"simple product has non-empty variations: {variations}")

    # product SKU uniqueness
    sku = item.get("sku")
    if sku:
        if sku in seen_skus:
            err(pid, f"duplicate product sku {sku!r} also on id={seen_skus[sku]}")
        else:
            seen_skus[sku] = pid

    # variation SKU uniqueness
    for v in [x for x in item.get("variations", []) if isinstance(x, dict)]:
        vsku = v.get("sku")
        if vsku:
            if vsku in seen_skus:
                err(pid, f"duplicate variation sku {vsku!r} (variation {v['id']}) also on id={seen_skus[vsku]}")
            else:
                seen_skus[vsku] = pid

# ── Summary ───────────────────────────────────────────────────────────────────
total_vars = sum(len([v for v in p.get("variations", []) if isinstance(v, dict)]) for p in items)
print(f"Verify: create-items — {len(items)} items, {total_vars} variations\n")

if errors:
    print(f"  FAILED — {len(errors)} error(s):\n")
    for e in errors:
        print(f"  [ERROR] {e}")
else:
    print(f"  PASSED — all checks clean")
