import copy
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

products_raw  = json.loads((data_dir / "reshape-products" / "products.json").read_text())
variations_raw = json.loads((data_dir / "reshape-variations" / "variations.json").read_text())

out_dir = data_dir / "create-items"
out_dir.mkdir(parents=True, exist_ok=True)

# ── Phase 1: Create items ─────────────────────────────────────────────────────

items = [copy.deepcopy(p) for p in products_raw]
items_by_id = {p["id"]: p for p in items}

for entry in variations_raw:
    product_id = entry["product_id"]
    product = items_by_id.get(product_id)
    if not product:
        continue

    expected_ids = set(product["variations"])

    replaced = {}
    for v in entry["variations"]:
        if v["id"] in expected_ids and v["parent_id"] == product_id:
            replaced[v["id"]] = v

    product["variations"] = [replaced.get(vid, vid) for vid in product["variations"]]

# ── Phase 2: Per-item checks ──────────────────────────────────────────────────

# SKU patterns that identify non-product WooCommerce entries (per brand)
JUNK_SKU_PREFIXES = {
    "bikershades": ["LABEL-", "TRYB4UB-"],
}
JUNK_SKU_SUFFIXES = {
    "bikershades": ["-RX", "HIGHRX"],
}

item_errors  = {}
sale_warnings = []

def flag(pid, msg):
    item_errors.setdefault(pid, []).append(msg)

junk_prefixes = JUNK_SKU_PREFIXES.get(brand_key, [])
junk_suffixes = JUNK_SKU_SUFFIXES.get(brand_key, [])

for item in items:
    pid = item["id"]

    sku = item.get("sku", "")
    if any(sku.startswith(p) for p in junk_prefixes) or any(sku.endswith(s) for s in junk_suffixes):
        flag(pid, f"non-product SKU: {sku!r}")
        continue

    if item["type"] != "variable":
        continue

    unreplaced = [v for v in item["variations"] if isinstance(v, int)]
    filled     = [v for v in item["variations"] if isinstance(v, dict)]

    # unreplaced IDs
    if unreplaced:
        flag(pid, f"unreplaced variation IDs: {unreplaced}")

    # no filled variations
    if not filled:
        flag(pid, "variable product has no filled variations")
        item["variations"] = []
        continue

    # attribute expansion: if variation attribute name matches a parent attribute,
    # add the option if missing. if name doesn't match any parent attribute, flag.
    parent_attr_map = {a["name"]: a for a in item.get("attributes", [])}
    for v in filled:
        for a in v.get("attributes", []):
            if a["name"] in parent_attr_map:
                if a["option"] not in parent_attr_map[a["name"]]["options"]:
                    parent_attr_map[a["name"]]["options"].append(a["option"])
            else:
                flag(pid, f"variation {v['id']} attribute '{a['name']}' not in parent attributes")
    item["attributes"] = list(parent_attr_map.values())

    # prune: remove options no variation uses, drop empty attributes
    used_options = {}
    for v in filled:
        for a in v.get("attributes", []):
            used_options.setdefault(a["name"], set()).add(a["option"])

    item["attributes"] = [
        {**attr, "options": [o for o in attr["options"] if o in used_options.get(attr["name"], set())]}
        for attr in item["attributes"]
        if any(o in used_options.get(attr["name"], set()) for o in attr["options"])
    ]

    # image dedup: remove variation images that duplicate a parent image
    parent_srcs = {img["src"] for img in item.get("images", [])}
    for v in filled:
        v["images"] = [img for img in v.get("images", []) if img["src"] not in parent_srcs]

    # min/max price + sale
    reg_prices = [v["regularPriceCents"] for v in filled if v.get("regularPriceCents") is not None]
    item["minPriceCents"] = min(reg_prices) if reg_prices else None
    item["maxPriceCents"] = max(reg_prices) if reg_prices else None

    computed_sale = any(v.get("sale") for v in filled)
    if computed_sale != item.get("sale"):
        sale_warnings.append(f"id={pid}: WC sale={item.get('sale')} computed={computed_sale}")
    item["sale"] = computed_sale

    item["variations"] = filled

# ── Phase 3: Global SKU uniqueness ───────────────────────────────────────────

seen_skus = {}

for item in items:
    pid = item["id"]

    sku = item.get("sku")
    if sku:
        if sku in seen_skus:
            flag(pid, f"duplicate sku {sku!r} also on product id={seen_skus[sku]}")
            flag(seen_skus[sku], f"duplicate sku {sku!r} also on product id={pid}")
        else:
            seen_skus[sku] = pid

    for v in [x for x in item.get("variations", []) if isinstance(x, dict)]:
        vsku = v.get("sku")
        if vsku:
            if vsku in seen_skus:
                flag(pid, f"duplicate sku {vsku!r} (variation {v['id']}) also on id={seen_skus[vsku]}")
            else:
                seen_skus[vsku] = pid

# ── Outputs ───────────────────────────────────────────────────────────────────

flagged_ids = set(item_errors)
valid   = [p for p in items if p["id"] not in flagged_ids]
flagged = [{"reasons": item_errors[p["id"]], "product": p} for p in items if p["id"] in flagged_ids]

(out_dir / "items.json").write_text(json.dumps(valid, indent=2, ensure_ascii=False))
(out_dir / "flagged.json").write_text(json.dumps(flagged, indent=2, ensure_ascii=False))

# ── Summary ───────────────────────────────────────────────────────────────────
total_vars   = sum(len(p.get("variations", [])) for p in valid if p["type"] == "variable")
total_issues = sum(len(v) for v in item_errors.values())

print(f"Combined {len(products_raw)} products\n")
print(f"  Passed:  {len(valid)}  ({total_vars} variations embedded)")
print(f"  Flagged: {len(flagged)}  ({total_issues} issues)\n")

if sale_warnings:
    print(f"── Sale cross-check warnings ({len(sale_warnings)}) ──")
    for w in sale_warnings:
        print(f"  [WARN] {w}")
    print()

for item in items:
    pid = item["id"]
    name = item.get("name", "")[:40]
    for msg in item_errors.get(pid, []):
        print(f"  [FLAG] id={pid} | {name} | {msg}")

print(f"\nSaved → {out_dir / 'items.json'} ({len(valid)} items)")
print(f"Saved → {out_dir / 'flagged.json'} ({len(flagged)} flagged)")
