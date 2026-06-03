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
products = json.loads((BASE / "data" / slug / "reshape-products" / "products.json").read_text())

variables = [p for p in products if p["type"] == "variable"]
simples   = [p for p in products if p["type"] == "simple"]

def pct(n, total):
    return f"{n}/{total} ({100*n/total:.1f}%)" if total else "0/0"

def filled(v):
    if v is None: return False
    if isinstance(v, list): return len(v) > 0
    return True

print(f"{'='*60}")
print(f"  RESHAPE PRODUCTS AUDIT — {brand_name}")
print(f"{'='*60}")
print(f"  Total:    {len(products)}")
print(f"  Variable: {len(variables)}")
print(f"  Simple:   {len(simples)}")

# ── Field presence ────────────────────────────────────────────────────────────
print(f"\n── Field presence ──")
fields = [
    "description", "descriptionImages", "summary",
    "weight", "images",
]
for f in fields:
    n = sum(1 for p in products if filled(p.get(f)))
    print(f"  {f:<22} {pct(n, len(products))}")
has_dims = sum(1 for p in products if any(p.get("dimensions", {}).get(d) is not None for d in ("length", "width", "height")))
print(f"  {'dimensions':<22} {pct(has_dims, len(products))}  (at least one non-null field)")

# ── Pricing ───────────────────────────────────────────────────────────────────
print(f"\n── Pricing (simple products) ──")
sale_on  = [p for p in simples if p.get("sale")]
sale_off = [p for p in simples if not p.get("sale")]
print(f"  sale=True:  {len(sale_on)}")
print(f"  sale=False: {len(sale_off)}")
if simples:
    prices = [p["minPriceCents"] for p in simples if p.get("minPriceCents")]
    print(f"  minPriceCents range: {min(prices)}–{max(prices)} cents  (${min(prices)/100:.2f}–${max(prices)/100:.2f})")
if sale_on:
    sale_prices = [p["salePriceCents"] for p in sale_on if p.get("salePriceCents")]
    print(f"  salePriceCents range: {min(sale_prices)}–{max(sale_prices)} cents")

print(f"\n── Pricing (variable products) ──")
print(f"  minPriceCents=null: {pct(sum(1 for p in variables if p['minPriceCents'] is None), len(variables))}")
print(f"  maxPriceCents=null: {pct(sum(1 for p in variables if p['maxPriceCents'] is None), len(variables))}")
print(f"  salePriceCents=null: {pct(sum(1 for p in variables if p['salePriceCents'] is None), len(variables))}")
var_sale_true = sum(1 for p in variables if p.get("sale"))
print(f"  sale=True (WC value, deferred): {pct(var_sale_true, len(variables))}")

# ── Stock ─────────────────────────────────────────────────────────────────────
print(f"\n── Stock ──")
stock_zero     = sum(1 for p in products if p.get("stock") == 0)
stock_pos      = sum(1 for p in products if isinstance(p.get("stock"), int) and p["stock"] > 0)
stock_one_flag = sum(1 for p in products if p.get("stock") == 1)
print(f"  stock=0 (outofstock / empty qty): {stock_zero}")
print(f"  stock=1 (instock fallback):        {stock_one_flag}")
print(f"  stock>1 (real quantity):           {stock_pos - stock_one_flag}")

# ── Weight ────────────────────────────────────────────────────────────────────
print(f"\n── Weight ──")
weights = [p["weight"] for p in products if p.get("weight") is not None]
print(f"  Non-null: {pct(len(weights), len(products))}")
if weights:
    print(f"  Range: {min(weights)}–{max(weights)}")

# ── Images ────────────────────────────────────────────────────────────────────
print(f"\n── Images ──")
img_counts = [len(p.get("images") or []) for p in products]
print(f"  Total image objects: {sum(img_counts)}")
print(f"  Per product — min: {min(img_counts)}  max: {max(img_counts)}  avg: {sum(img_counts)/len(img_counts):.1f}")
print(f"  Products with no images: {sum(1 for c in img_counts if c == 0)}")

# ── Descriptions ─────────────────────────────────────────────────────────────
print(f"\n── Description images ──")
di_counts = Counter(len(p.get("descriptionImages") or []) for p in products)
for count in sorted(di_counts):
    label = f"{count} image{'s' if count != 1 else ''}"
    print(f"  {label}: {di_counts[count]} products")

print(f"\n── Short description ──")
sd_counts = [len(p.get("summary") or []) for p in products if p.get("summary")]
print(f"  Has summary: {pct(len(sd_counts), len(products))}")
if sd_counts:
    print(f"  Bullets per product — min: {min(sd_counts)}  max: {max(sd_counts)}  avg: {sum(sd_counts)/len(sd_counts):.1f}")

# ── Categories ────────────────────────────────────────────────────────────────
print(f"\n── Categories ──")
cat_counter = Counter(c["name"] for p in products for c in p.get("categories", []))
print(f"  Unique categories: {len(cat_counter)}")
print(f"  Products with no categories: {sum(1 for p in products if not p.get('categories'))}")
for name, count in cat_counter.most_common(10):
    print(f"  {count:>4}  {name}")
if len(cat_counter) > 10:
    print(f"  ... and {len(cat_counter) - 10} more")

# ── Attributes ────────────────────────────────────────────────────────────────
print(f"\n── Attributes ──")
attr_counter = Counter(a["name"] for p in products for a in p.get("attributes", []))
for name, count in attr_counter.most_common():
    option_set = {o for p in products for a in p.get("attributes", []) if a["name"] == name for o in a.get("options", [])}
    print(f"  {name:<30} {count:>4} products  {len(option_set):>4} unique options")
multi_word = [n for n in attr_counter if ' ' in n]
if multi_word:
    print(f"  [WARN] multi-word attribute names: {multi_word}")
else:
    print(f"  all attribute names are single-word ✓")
