import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from config import BASE, load_brand

_, config = load_brand()
slug = config["slug"]
raw = json.loads((BASE / f"data/{slug}/slim-variations/variations.json").read_text())

all_v = [v for e in raw for v in e["variations"]]
N = len(all_v)
n_products = len(raw)

print(f"=== Slim Variations ({N} total across {n_products} products) ===\n")

# ── Field presence ─────────────────────────────────────────────────────────────
def filled(v, field):
    val = v.get(field)
    if field == "dimensions":
        return isinstance(val, dict) and all(val.get(k, "") not in ("", None) for k in ("length", "width", "height"))
    if field == "image":
        return isinstance(val, dict) and bool(val.get("src"))
    if field == "attributes":
        return isinstance(val, list) and len(val) > 0
    return val not in (None, "", [], {}, "0.00")

print("Field presence:")
for field in all_v[0].keys():
    n = sum(1 for v in all_v if filled(v, field))
    missing = N - n
    print(f"  {field:<20} {n:>5}/{N}  {'OK' if n == N else f'MISSING {missing}'}")

# ── Flags ──────────────────────────────────────────────────────────────────────
print("\n--- flags ---")
no_sku      = [v for v in all_v if not v.get("sku")]
no_price    = [v for v in all_v if not v.get("price")]
non_publish = [v for v in all_v if v.get("status") != "publish"]

print(f"  No SKU:        {len(no_sku)}")
for v in no_sku:
    print(f"    id={v['id']} parent={v['parent_id']} name={v.get('name', '')[:50]}")

print(f"  No price:      {len(no_price)}")
for v in no_price:
    print(f"    id={v['id']} parent={v['parent_id']} sku={v.get('sku')} stock_status={v.get('stock_status')}")

print(f"  Non-publish:   {len(non_publish)}")
for v in non_publish:
    print(f"    id={v['id']} parent={v['parent_id']} status={v.get('status')}")

# ── on_sale truthfulness ──────────────────────────────────────────────────────
print("\n--- on_sale vs sale_price ---")
on_sale_no_price  = [v for v in all_v if v.get("on_sale") and not v.get("sale_price")]
has_price_no_sale = [v for v in all_v if v.get("sale_price") and not v.get("on_sale")]
print(f"  on_sale=True but no sale_price:   {len(on_sale_no_price)}")
for v in on_sale_no_price[:5]:
    print(f"    id={v['id']} price={v.get('price')} regular={v.get('regular_price')}")
print(f"  has sale_price but on_sale=False: {len(has_price_no_sale)}")
for v in has_price_no_sale[:5]:
    print(f"    id={v['id']} sale={v.get('sale_price')} regular={v.get('regular_price')}")

# ── stock_quantity vs stock_status ────────────────────────────────────────────
print("\n--- stock_quantity vs stock_status ---")
combos = Counter(
    (v["stock_quantity"] is not None, v.get("stock_status"))
    for v in all_v
)
print("  (has_qty, stock_status):")
for (has_qty, status), n in sorted(combos.items()):
    print(f"    has_qty={has_qty}  stock_status={status:<12}  {n} variations")

# ── Attributes ────────────────────────────────────────────────────────────────
print("\n--- attributes ---")
attr_counts = Counter(len(v.get("attributes", [])) for v in all_v)
attr_name_usage = Counter(a["name"] for v in all_v for a in v.get("attributes", []))
print(f"  Attribute count distribution: {dict(sorted(attr_counts.items()))}")
print(f"  Unique attribute names: {len(attr_name_usage)}")
for name, n in attr_name_usage.most_common():
    print(f"    {name}: {n} variations")

# ── Image ─────────────────────────────────────────────────────────────────────
print("\n--- image ---")
has_image = sum(1 for v in all_v if filled(v, "image"))
print(f"  Has image src: {has_image} / {N}")

# ── Weight ────────────────────────────────────────────────────────────────────
print("\n--- weight ---")
weight_vals = Counter(v.get("weight") for v in all_v if v.get("weight") not in (None, ""))
print(f"  Has weight: {sum(1 for v in all_v if v.get('weight') not in (None, ''))} / {N}")
print(f"  Value distribution: {dict(weight_vals.most_common(5))}")

# ── parent_id cross-check ─────────────────────────────────────────────────────
print("\n--- parent_id cross-check ---")
mismatches = [
    v for e in raw for v in e["variations"]
    if v["parent_id"] != e["product_id"]
]
print(f"  Variations where parent_id != product_id key: {len(mismatches)}")
