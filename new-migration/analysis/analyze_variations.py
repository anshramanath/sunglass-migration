import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from config import BASE, load_brand

_, config = load_brand()
slug = config["slug"]
raw = json.loads((BASE / f"data/{slug}/fetch-variations/variations.json").read_text())

# Flatten while keeping per-product structure available
all_variations = [v for entry in raw for v in entry["variations"]]
total = len(all_variations)
n_products = len(raw)

# ── Overview ──────────────────────────────────────────────────────────────────
print(f"=== Variations ({total} total across {n_products} products) ===\n")

counts = [len(e["variations"]) for e in raw]
print(f"Per-product variation counts:")
print(f"  min={min(counts)}  max={max(counts)}  avg={sum(counts)/len(counts):.1f}")
dist = Counter(counts)
print(f"  Distribution (count: products): ", end="")
print("  ".join(f"{k}:{v}" for k, v in sorted(dist.items())))

# ── Status ────────────────────────────────────────────────────────────────────
statuses = Counter(v["status"] for v in all_variations)
print(f"\nStatuses:")
for s, n in statuses.most_common():
    print(f"  {s}: {n}")

# ── SKUs ──────────────────────────────────────────────────────────────────────
all_skus = [v["sku"] for v in all_variations if v.get("sku")]
dup_skus = {sku for sku, n in Counter(all_skus).items() if n > 1}
no_sku = [v for v in all_variations if not v.get("sku")]
print(f"\nSKUs:")
print(f"  Total:       {len(all_skus)} / {total}")
print(f"  Unique:      {len(set(all_skus))}")
print(f"  Duplicates:  {len(dup_skus)}")
print(f"  Missing SKU: {len(no_sku)}")
for v in no_sku[:5]:
    print(f"    id={v['id']} parent={v['parent_id']} name={v.get('name', '')[:50]}")

# ── Pricing ───────────────────────────────────────────────────────────────────
has_price    = sum(1 for v in all_variations if v.get("price"))
has_regular  = sum(1 for v in all_variations if v.get("regular_price"))
has_sale     = sum(1 for v in all_variations if v.get("sale_price"))
on_sale_true = sum(1 for v in all_variations if v.get("on_sale"))
on_sale_with_price = sum(1 for v in all_variations if v.get("on_sale") and v.get("sale_price"))
on_sale_no_price   = sum(1 for v in all_variations if v.get("on_sale") and not v.get("sale_price"))

print(f"\nPricing:")
print(f"  Has price:          {has_price} / {total}")
print(f"  Has regular_price:  {has_regular} / {total}")
print(f"  Has sale_price:     {has_sale} / {total}")
print(f"  on_sale=True:       {on_sale_true} / {total}")
print(f"    with sale_price:  {on_sale_with_price}")
print(f"    no sale_price:    {on_sale_no_price}")

# ── Stock ─────────────────────────────────────────────────────────────────────
manage_stock_true = sum(1 for v in all_variations if v.get("manage_stock"))
has_qty           = sum(1 for v in all_variations if v.get("stock_quantity") is not None)
stock_statuses    = Counter(v.get("stock_status") for v in all_variations)

print(f"\nStock:")
print(f"  manage_stock=True:  {manage_stock_true} / {total}")
print(f"  Has stock_quantity: {has_qty} / {total}")
print(f"  stock_status: {dict(stock_statuses)}")

# Cross-check
combos = Counter(
    (v.get("stock_quantity") is not None, v.get("stock_status"))
    for v in all_variations
)
print(f"  Combinations (has_qty, status):")
for (has_q, ss), n in sorted(combos.items()):
    print(f"    qty={'yes' if has_q else 'no'} + {ss}: {n}")

# ── Images ────────────────────────────────────────────────────────────────────
has_image    = sum(1 for v in all_variations if v.get("image") and v["image"].get("src"))
no_image     = sum(1 for v in all_variations if not v.get("image") or not v["image"].get("src"))
print(f"\nImages (singular `image` field):")
print(f"  Has image src: {has_image} / {total}")
print(f"  No image:      {no_image}")

# ── Attributes ────────────────────────────────────────────────────────────────
attr_name_usage  = Counter(a["name"] for v in all_variations for a in v.get("attributes", []))
attr_counts      = Counter(len(v.get("attributes", [])) for v in all_variations)
no_attrs         = sum(1 for v in all_variations if not v.get("attributes"))

print(f"\nAttributes (per-variation chosen options):")
print(f"  Variations with no attributes: {no_attrs}")
print(f"  Attribute count distribution:  {dict(sorted(attr_counts.items()))}")
print(f"  Unique attribute names ({len(attr_name_usage)}):")
for name, n in attr_name_usage.most_common():
    print(f"    {name}: {n} variations")

# ── Weight / Dimensions ───────────────────────────────────────────────────────
has_weight = sum(1 for v in all_variations if v.get("weight") not in (None, ""))
def dims_filled(v):
    d = v.get("dimensions", {})
    return all(d.get(k, "") not in ("", None) for k in ("length", "width", "height"))

print(f"\nWeight / Dimensions:")
print(f"  Has weight:               {has_weight} / {total}")
print(f"  Dimensions fully filled:  {sum(1 for v in all_variations if dims_filled(v))} / {total}")

# ── Description / Name ────────────────────────────────────────────────────────
has_desc = sum(1 for v in all_variations if v.get("description", "").strip())
print(f"\nDescription / Name:")
print(f"  Has description: {has_desc} / {total}")
sample_names = [v["name"] for v in all_variations[:5] if v.get("name")]
print(f"  Sample names:")
for n in sample_names:
    print(f"    {n}")

# ── Field coverage ────────────────────────────────────────────────────────────
def is_meaningful(field, val):
    if val is None:
        return False
    if field == "dimensions":
        return isinstance(val, dict) and all(val.get(k, "") not in ("", None) for k in ("length", "width", "height"))
    if field == "image":
        return isinstance(val, dict) and bool(val.get("src"))
    if val in ("", [], {}, 0, "0.00", "taxable", "no", False):
        return False
    if isinstance(val, bool):
        return val
    return True

def summarize(val):
    if val is None:
        return "null"
    if isinstance(val, list):
        return f"list[{len(val)}]" if val else "[]"
    if isinstance(val, dict):
        return "{...}" if val else "{}"
    if isinstance(val, bool):
        return str(val)
    s = str(val).strip()
    if not s:
        return '""'
    return s[:60] + ("…" if len(s) > 60 else "")

SKIP = {"_links"}
fields = [k for k in all_variations[0].keys() if k not in SKIP]

print(f"\n\n=== Field coverage ({total} variations) ===\n")
print(f"{'field':<30} {'filled':>6}  {'%':>5}  top values")
print("-" * 90)

for field in fields:
    values = [v.get(field) for v in all_variations]
    filled = sum(1 for val in values if is_meaningful(field, val))
    pct = filled / total * 100
    top = Counter(summarize(val) for val in values).most_common(4)
    top_str = "  ".join(f"{label}×{n}" for label, n in top)
    print(f"{field:<30} {filled:>6}  {pct:>4.0f}%  {top_str}")
