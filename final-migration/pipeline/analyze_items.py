import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from config import BASE, load_brand

brand_key, config = load_brand()
slug = config["slug"]

in_path = BASE / "data" / slug / "validate-items" / "items.json"
if not in_path.exists():
    raise SystemExit(f"Run validate_items.py first. Not found: {in_path}")

items = json.loads(in_path.read_text())

simple   = [i for i in items if i.get("sku") is not None]
variable = [i for i in items if i.get("sku") is None]

def pct(n, total):
    return f"{n / total * 100:.1f}%" if total else "0%"

def price_str(cents):
    return f"${cents / 100:.2f}" if cents is not None else "null"

def stats(values):
    if not values:
        return "n/a"
    return f"min={price_str(min(values))}  max={price_str(max(values))}  avg={price_str(round(sum(values)/len(values)))}"

def section(title):
    print(f"\n{'─' * 60}")
    print(f"  {title}")
    print(f"{'─' * 60}")

# ── Overview ──────────────────────────────────────────────────
section("OVERVIEW")
print(f"  Brand:    {config['brand_name']} ({slug})")
print(f"  Total:    {len(items)}")
print(f"  Simple:   {len(simple)}  ({pct(len(simple), len(items))})")
print(f"  Variable: {len(variable)}  ({pct(len(variable), len(items))})")

# ── Stock & Availability ──────────────────────────────────────
section("STOCK & AVAILABILITY")

simple_in  = [i for i in simple   if i.get("inStock")]
simple_out = [i for i in simple   if not i.get("inStock")]
var_in     = [i for i in variable if i.get("inStock")]
var_out    = [i for i in variable if not i.get("inStock")]

print(f"  Simple   in stock:  {len(simple_in)}  ({pct(len(simple_in), len(simple))})")
print(f"  Simple   out:       {len(simple_out)}  ({pct(len(simple_out), len(simple))})")
print(f"  Variable in stock:  {len(var_in)}  ({pct(len(var_in), len(variable))})")
print(f"  Variable out:       {len(var_out)}  ({pct(len(var_out), len(variable))})")

simple_stocks = [i["stock"] for i in simple if isinstance(i.get("stock"), int)]
if simple_stocks:
    print(f"\n  Simple stock  min={min(simple_stocks)}  max={max(simple_stocks)}  avg={round(sum(simple_stocks)/len(simple_stocks))}")

all_var_stocks = [v["stock"] for i in variable for v in i.get("variations", []) if isinstance(v.get("stock"), int)]
if all_var_stocks:
    print(f"  Variation stock  min={min(all_var_stocks)}  max={max(all_var_stocks)}  avg={round(sum(all_var_stocks)/len(all_var_stocks))}")
    zero_stock_vars = sum(1 for s in all_var_stocks if s == 0)
    print(f"  Variations at 0 stock: {zero_stock_vars}  ({pct(zero_stock_vars, len(all_var_stocks))})")

# ── Pricing ───────────────────────────────────────────────────
section("PRICING")

simple_prices = [i["minPriceCents"] for i in simple if isinstance(i.get("minPriceCents"), int)]
var_min_prices = [i["minPriceCents"] for i in variable if isinstance(i.get("minPriceCents"), int)]
var_max_prices = [i["maxPriceCents"] for i in variable if isinstance(i.get("maxPriceCents"), int)]

print(f"  Simple prices ({len(simple_prices)} products):  {stats(simple_prices)}")
free_simple = [i["name"] for i in simple if i.get("minPriceCents") == 0]
if free_simple:
    print(f"  Free simple products ({len(free_simple)}):")
    for n in free_simple:
        print(f"    - {n}")

print(f"\n  Variable minPrice ({len(var_min_prices)} products):  {stats(var_min_prices)}")
print(f"  Variable maxPrice ({len(var_max_prices)} products):  {stats(var_max_prices)}")

spread = [(i["name"], i["maxPriceCents"] - i["minPriceCents"])
          for i in variable
          if isinstance(i.get("minPriceCents"), int) and isinstance(i.get("maxPriceCents"), int)
          and i["maxPriceCents"] != i["minPriceCents"]]
print(f"\n  Variable products with price spread (min ≠ max): {len(spread)}")
if spread:
    spread.sort(key=lambda x: -x[1])
    for name, diff in spread[:5]:
        print(f"    {price_str(diff):>10} spread  —  {name}")
    if len(spread) > 5:
        print(f"    ... and {len(spread) - 5} more")

all_var_prices = [v["regularPriceCents"] for i in variable for v in i.get("variations", []) if isinstance(v.get("regularPriceCents"), int)]
print(f"\n  All variation prices ({len(all_var_prices)}):  {stats(all_var_prices)}")
free_vars = sum(1 for p in all_var_prices if p == 0)
if free_vars:
    print(f"  Free variations: {free_vars}")

# ── Variations ────────────────────────────────────────────────
section("VARIATIONS")

total_variations = sum(len(i.get("variations", [])) for i in variable)
var_counts = [len(i.get("variations", [])) for i in variable]
print(f"  Total variations across all variable products: {total_variations}")
print(f"  Per product  min={min(var_counts)}  max={max(var_counts)}  avg={round(sum(var_counts)/len(var_counts)) if var_counts else 0}")

buckets = Counter()
for c in var_counts:
    if c <= 5:       buckets["2-5"] += 1
    elif c <= 10:    buckets["6-10"] += 1
    elif c <= 25:    buckets["11-25"] += 1
    elif c <= 50:    buckets["26-50"] += 1
    else:            buckets["51+"] += 1
for label in ["2-5", "6-10", "11-25", "26-50", "51+"]:
    n = buckets[label]
    if n:
        print(f"    {label:>6} variations: {n} products")

# ── Attributes ────────────────────────────────────────────────
section("ATTRIBUTES")

all_attr_names = Counter()
for i in variable:
    for a in i.get("attributes", []):
        all_attr_names[a["name"]] += 1

multi_attr = [i for i in variable if len(i.get("attributes", [])) > 1]
no_attr    = [i for i in variable if not i.get("attributes")]

print(f"  Variable products with >1 attribute:  {len(multi_attr)}")
print(f"  Variable products with no attributes: {len(no_attr)}")
if no_attr:
    for i in no_attr:
        print(f"    - {i['name']}")

print(f"\n  Top attribute names:")
for name, count in all_attr_names.most_common(10):
    print(f"    {count:>4}x  {name}")

# ── Images ────────────────────────────────────────────────────
section("IMAGES")

no_product_images    = [i["name"] for i in items if not i.get("productImages")]
has_desc_images      = [i["name"] for i in items if i.get("descriptionImages")]
product_image_counts = [len(i.get("productImages", [])) for i in items]

print(f"  Products with no product images:      {len(no_product_images)}  ({pct(len(no_product_images), len(items))})")
if no_product_images:
    for n in no_product_images[:5]:
        print(f"    - {n}")
    if len(no_product_images) > 5:
        print(f"    ... and {len(no_product_images) - 5} more")

print(f"  Products with description images:     {len(has_desc_images)}  ({pct(len(has_desc_images), len(items))})")
print(f"  Product image count  min={min(product_image_counts)}  max={max(product_image_counts)}  avg={round(sum(product_image_counts)/len(product_image_counts)) if product_image_counts else 0}")

var_no_images = sum(1 for i in variable for v in i.get("variations", []) if not v.get("variationImages"))
var_total     = sum(len(i.get("variations", [])) for i in variable)
print(f"  Variations with no image:             {var_no_images} / {var_total}  ({pct(var_no_images, var_total)})")

# ── Content (description / summary) ───────────────────────────
section("CONTENT  [deferred fields — not yet populated]")

null_desc    = [i["name"] for i in items if i.get("description") is None]
empty_sum    = [i["name"] for i in items if not i.get("summary")]
both_missing = [i["name"] for i in items if i.get("description") is None and not i.get("summary")]
has_both     = [i["name"] for i in items if i.get("description") and i.get("summary")]

print(f"  Null description:              {len(null_desc)}  ({pct(len(null_desc), len(items))})")
print(f"  Empty summary:                 {len(empty_sum)}  ({pct(len(empty_sum), len(items))})")
print(f"  Missing both desc + summary:   {len(both_missing)}  ({pct(len(both_missing), len(items))})")
print(f"  Has both desc + summary:       {len(has_both)}  ({pct(len(has_both), len(items))})")

summary_lengths = [len(i["summary"]) for i in items if i.get("summary")]
if summary_lengths:
    print(f"  Summary items per product (when present):  min={min(summary_lengths)}  max={max(summary_lengths)}  avg={round(sum(summary_lengths)/len(summary_lengths))}")

print()
