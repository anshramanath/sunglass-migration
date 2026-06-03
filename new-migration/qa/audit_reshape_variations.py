import json
import os
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from config import BASE, load_brand


brand_key, config = load_brand()
slug       = config["slug"]
brand_name = config["brand_name"]
data = json.loads((BASE / "data" / slug / "reshape-variations" / "variations.json").read_text())

all_vars = [v for e in data for v in e["variations"]]
total_products = len(data)
total_vars = len(all_vars)

def pct(n, total):
    return f"{n}/{total} ({100*n/total:.1f}%)" if total else "0/0"

print(f"{'='*60}")
print(f"  RESHAPE VARIATIONS AUDIT — {brand_name}")
print(f"{'='*60}")
print(f"  Products with variations: {total_products}")
print(f"  Total variations:         {total_vars}")

# ── Field presence ────────────────────────────────────────────────────────────
print(f"\n── Field presence ──")
for field in ("description", "weight"):
    n = sum(1 for v in all_vars if v.get(field) is not None)
    print(f"  {field:<14} {pct(n, total_vars)}")

has_dims = sum(1 for v in all_vars if any(v.get("dimensions", {}).get(d) is not None for d in ("length", "width", "height")))
print(f"  {'dimensions':<14} {pct(has_dims, total_vars)}  (at least one non-null field)")

# ── Pricing ───────────────────────────────────────────────────────────────────
print(f"\n── Pricing ──")
sale_on  = [v for v in all_vars if v.get("sale")]
sale_off = [v for v in all_vars if not v.get("sale")]
print(f"  sale=True:  {len(sale_on)}")
print(f"  sale=False: {len(sale_off)}")

reg_prices = [v["regularPriceCents"] for v in all_vars if v.get("regularPriceCents")]
print(f"  regularPriceCents range: {min(reg_prices)}–{max(reg_prices)} (${min(reg_prices)/100:.2f}–${max(reg_prices)/100:.2f})")

if sale_on:
    sale_prices = [v["salePriceCents"] for v in sale_on if v.get("salePriceCents")]
    print(f"  salePriceCents range:    {min(sale_prices)}–{max(sale_prices)} (${min(sale_prices)/100:.2f}–${max(sale_prices)/100:.2f})")

null_reg = sum(1 for v in all_vars if v.get("regularPriceCents") is None)
null_sale = sum(1 for v in all_vars if v.get("salePriceCents") is None)
print(f"  regularPriceCents=null: {null_reg}")
print(f"  salePriceCents=null:    {null_sale}")

# ── Stock ─────────────────────────────────────────────────────────────────────
print(f"\n── Stock ──")
stock_zero = sum(1 for v in all_vars if v.get("stock") == 0)
stock_one  = sum(1 for v in all_vars if v.get("stock") == 1)
stock_pos  = sum(1 for v in all_vars if isinstance(v.get("stock"), int) and v["stock"] > 1)
print(f"  stock=0 (outofstock / zero qty): {stock_zero}")
print(f"  stock=1 (instock fallback):       {stock_one}")
print(f"  stock>1 (real quantity):          {stock_pos}")

# ── Weight ────────────────────────────────────────────────────────────────────
print(f"\n── Weight ──")
weights = [v["weight"] for v in all_vars if v.get("weight") is not None]
print(f"  Non-null: {pct(len(weights), total_vars)}")
if weights:
    print(f"  Range: {min(weights)}–{max(weights)}")

# ── Images ────────────────────────────────────────────────────────────────────
print(f"\n── Images ──")
with_img  = sum(1 for v in all_vars if v.get("images"))
no_img    = sum(1 for v in all_vars if not v.get("images"))
print(f"  images non-empty : {pct(with_img, total_vars)}")
print(f"  images empty     : {no_img}  (null source image)")
unique_srcs = {img["src"] for v in all_vars for img in v.get("images", [])}
print(f"  unique image URLs: {len(unique_srcs)}")

# ── Attributes ────────────────────────────────────────────────────────────────
print(f"\n── Attributes ──")
attr_counter = Counter(a["name"] for v in all_vars for a in v.get("attributes", []))
for name, count in attr_counter.most_common():
    options = {a["option"] for v in all_vars for a in v.get("attributes", []) if a["name"] == name}
    print(f"  {name:<12} {count:>6} variations  {len(options):>4} unique options")
multi_word = [n for n in attr_counter if ' ' in n]
if multi_word:
    print(f"  [WARN] multi-word attribute names: {multi_word}")
else:
    print(f"  all attribute names are single-word ✓")

# ── Variations per product ────────────────────────────────────────────────────
print(f"\n── Variations per product ──")
counts = sorted(len(e["variations"]) for e in data)
print(f"  min: {min(counts)}  max: {max(counts)}  avg: {sum(counts)/len(counts):.1f}")
buckets = Counter(c for c in counts)
for n in sorted(buckets):
    print(f"  {n:>3} variations: {buckets[n]} products")
