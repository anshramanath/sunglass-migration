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
all_variations = [v for i in variable for v in i.get("variations", [])]

def pct(n, total):
    return f"{n / total * 100:.1f}%" if total else "0.0%"

def dollars(cents):
    return f"${cents / 100:.2f}" if cents is not None else "null"

def price_stats(values, label=""):
    if not values:
        return f"{label}n/a"
    return (f"{label}min={dollars(min(values))}  "
            f"max={dollars(max(values))}  "
            f"avg={dollars(round(sum(values)/len(values)))}")

def count_stats(values, label=""):
    if not values:
        return f"{label}n/a"
    return (f"{label}min={min(values)}  max={max(values)}  "
            f"avg={round(sum(values)/len(values), 1)}")

def section(title):
    print(f"\n{'─' * 64}")
    print(f"  {title}")
    print(f"{'─' * 64}")

def bucket_dist(values, thresholds, labels):
    counts = Counter()
    for v in values:
        for t, lbl in zip(thresholds, labels):
            if v <= t:
                counts[lbl] += 1
                break
        else:
            counts[labels[-1]] += 1
    for lbl in labels:
        if counts[lbl]:
            print(f"    {lbl:>12}: {counts[lbl]}")

# ── Overview ──────────────────────────────────────────────────
section("OVERVIEW")
print(f"  Brand:    {config['brand_name']} ({slug})")
print(f"  Total:    {len(items)}")
print(f"  Simple:   {len(simple)}  ({pct(len(simple), len(items))})")
print(f"  Variable: {len(variable)}  ({pct(len(variable), len(items))})")

# ── SKU ───────────────────────────────────────────────────────
section("SKU")
simple_skus = [i["sku"] for i in simple]
dup_skus = [sku for sku, n in Counter(simple_skus).items() if n > 1]
print(f"  Simple products with SKU: {len(simple_skus)}")
print(f"  Duplicate SKUs:           {len(dup_skus)}")
if dup_skus:
    for s in dup_skus:
        print(f"    {s!r}")
var_skus = [v["sku"] for v in all_variations]
dup_var_skus = [sku for sku, n in Counter(var_skus).items() if n > 1]
print(f"  Variation SKUs total:     {len(var_skus)}")
print(f"  Duplicate variation SKUs: {len(dup_var_skus)}")
if dup_var_skus:
    for s in dup_var_skus[:5]:
        print(f"    {s!r}")

# ── Name ──────────────────────────────────────────────────────
section("NAME")
name_lengths = [len(i["name"]) for i in items]
dup_names = [n for n, c in Counter(i["name"] for i in items).items() if c > 1]
print(f"  {count_stats(name_lengths, 'Length  ')}")
print(f"  Duplicate names: {len(dup_names)}")
if dup_names:
    for n in dup_names:
        print(f"    {n!r}")

# ── Slug ──────────────────────────────────────────────────────
section("SLUG")
dup_slugs = [s for s, c in Counter(i["slug"] for i in items).items() if c > 1]
print(f"  Duplicate slugs: {len(dup_slugs)}")
if dup_slugs:
    for s in dup_slugs:
        print(f"    {s!r}")

# ── Featured ──────────────────────────────────────────────────
section("FEATURED")
not_false = [i["name"] for i in items if i.get("featured") is not False]
print(f"  All false: {len(not_false) == 0}")
if not_false:
    for n in not_false:
        print(f"    {n}")

# ── Sale / SalePriceCents ─────────────────────────────────────
section("SALE / SALE PRICE CENTS")
sale_true    = [i["name"] for i in items if i.get("sale") is not False]
sale_price   = [i["name"] for i in items if i.get("salePriceCents") is not None]
v_sale_true  = [(i["name"], v["sku"]) for i in variable for v in i.get("variations", []) if v.get("sale") is not False]
v_sale_price = [(i["name"], v["sku"]) for i in variable for v in i.get("variations", []) if v.get("salePriceCents") is not None]
print(f"  Products with sale=true:           {len(sale_true)}")
print(f"  Products with salePriceCents set:  {len(sale_price)}")
print(f"  Variations with sale=true:         {len(v_sale_true)}")
print(f"  Variations with salePriceCents set:{len(v_sale_price)}")

# ── Categories ────────────────────────────────────────────────
section("CATEGORIES")
non_empty = [i["name"] for i in items if i.get("categories") != []]
print(f"  All empty: {len(non_empty) == 0}  (deferred field)")
if non_empty:
    for n in non_empty:
        print(f"    {n}")

# ── Stock & inStock ───────────────────────────────────────────
section("STOCK & INSTOCK")
simple_in  = [i for i in simple   if i.get("inStock")]
simple_out = [i for i in simple   if not i.get("inStock")]
var_in     = [i for i in variable if i.get("inStock")]
var_out    = [i for i in variable if not i.get("inStock")]
print(f"  Simple   in stock:  {len(simple_in)}  ({pct(len(simple_in), len(simple))})")
print(f"  Simple   out:       {len(simple_out)}  ({pct(len(simple_out), len(simple))})")
print(f"  Variable in stock:  {len(var_in)}  ({pct(len(var_in), len(variable))})")
print(f"  Variable out:       {len(var_out)}  ({pct(len(var_out), len(variable))})")

simple_stocks = [i["stock"] for i in simple if isinstance(i.get("stock"), int) and not isinstance(i.get("stock"), bool)]
if simple_stocks:
    print(f"\n  {count_stats(simple_stocks, 'Simple stock  ')}")
    neg = [i["name"] for i in simple if isinstance(i.get("stock"), int) and not isinstance(i.get("stock"), bool) and i["stock"] < 0]
    if neg:
        print(f"  Negative stock ({len(neg)}): {neg}")

var_stocks = [v["stock"] for v in all_variations if isinstance(v.get("stock"), int) and not isinstance(v.get("stock"), bool)]
if var_stocks:
    print(f"  {count_stats(var_stocks, 'Variation stock  ')}")
    zero  = sum(1 for s in var_stocks if s == 0)
    neg_v = sum(1 for s in var_stocks if s < 0)
    print(f"  Variations at 0:        {zero}  ({pct(zero, len(var_stocks))})")
    if neg_v:
        print(f"  Variations negative:    {neg_v}  ({pct(neg_v, len(var_stocks))})")

# ── Total Sales ───────────────────────────────────────────────
section("TOTAL SALES")
simple_ts_wrong   = [i["name"] for i in simple   if i.get("totalSales") != 0]
variable_ts_wrong = [i["name"] for i in variable  if i.get("totalSales") is not None]
var_ts_wrong      = [(i["name"], v["sku"]) for i in variable for v in i.get("variations", []) if v.get("totalSales") != 0]
print(f"  Simple totalSales != 0:       {len(simple_ts_wrong)}")
print(f"  Variable totalSales != null:  {len(variable_ts_wrong)}")
print(f"  Variation totalSales != 0:    {len(var_ts_wrong)}")

# ── Pricing ───────────────────────────────────────────────────
section("PRICING")
simple_prices = [i["minPriceCents"] for i in simple if isinstance(i.get("minPriceCents"), int) and not isinstance(i.get("minPriceCents"), bool)]
print(f"  Simple ({len(simple_prices)} with price):  {price_stats(simple_prices)}")
print(f"  Price distribution:")
bucket_dist(simple_prices,
    [500, 1000, 2000, 5000, 10000, 999999],
    ["$0-$5", "$5-$10", "$10-$20", "$20-$50", "$50-$100", "$100+"])

var_min = [i["minPriceCents"] for i in variable if isinstance(i.get("minPriceCents"), int) and not isinstance(i.get("minPriceCents"), bool)]
var_max = [i["maxPriceCents"] for i in variable if isinstance(i.get("maxPriceCents"), int) and not isinstance(i.get("maxPriceCents"), bool)]
print(f"\n  Variable minPriceCents ({len(var_min)}):  {price_stats(var_min)}")
print(f"  Variable maxPriceCents ({len(var_max)}):  {price_stats(var_max)}")

spread = [(i["name"], i["maxPriceCents"] - i["minPriceCents"])
          for i in variable
          if isinstance(i.get("minPriceCents"), int) and isinstance(i.get("maxPriceCents"), int)
          and i["maxPriceCents"] != i["minPriceCents"]]
spread.sort(key=lambda x: -x[1])
print(f"  Variable products with price spread: {len(spread)}")
for name, diff in spread[:5]:
    print(f"    {dollars(diff):>10} spread  —  {name}")
if len(spread) > 5:
    print(f"    ... and {len(spread) - 5} more")

var_prices = [v["regularPriceCents"] for v in all_variations if isinstance(v.get("regularPriceCents"), int) and not isinstance(v.get("regularPriceCents"), bool)]
print(f"\n  All variation regularPriceCents ({len(var_prices)}):  {price_stats(var_prices)}")
print(f"  Distribution:")
bucket_dist(var_prices,
    [500, 1000, 2000, 5000, 10000, 999999],
    ["$0-$5", "$5-$10", "$10-$20", "$20-$50", "$50-$100", "$100+"])

# ── Product Images ────────────────────────────────────────────
section("PRODUCT IMAGES")
no_images   = [i["name"] for i in items if not i.get("productImages")]
img_counts  = [len(i.get("productImages", [])) for i in items]
print(f"  Products with no images:  {len(no_images)}")
if no_images:
    for n in no_images:
        print(f"    - {n}")
print(f"  {count_stats(img_counts, 'Images per product  ')}")
print(f"  Distribution:")
bucket_dist(img_counts, [0, 1, 2, 3, 5, 999], ["0", "1", "2", "3", "4-5", "6+"])

# ── Description Images ────────────────────────────────────────
section("DESCRIPTION IMAGES")
has_desc_imgs  = [i for i in items if i.get("descriptionImages")]
desc_img_counts = [len(i.get("descriptionImages", [])) for i in items]
print(f"  Products with description images: {len(has_desc_imgs)}  ({pct(len(has_desc_imgs), len(items))})")
print(f"  {count_stats([c for c in desc_img_counts if c > 0], 'Count when present  ')}")
print(f"  Distribution:")
bucket_dist(desc_img_counts, [0, 2, 5, 10, 20, 999], ["0", "1-2", "3-5", "6-10", "11-20", "21+"])

# ── Description ───────────────────────────────────────────────
section("DESCRIPTION  [deferred]")
null_desc = [i for i in items if i.get("description") is None]
has_desc  = [i for i in items if i.get("description")]
desc_lens = [len(i["description"]) for i in has_desc]
print(f"  Null:    {len(null_desc)}  ({pct(len(null_desc), len(items))})")
print(f"  Present: {len(has_desc)}  ({pct(len(has_desc), len(items))})")
if desc_lens:
    print(f"  {count_stats(desc_lens, 'Length (chars)  ')}")

# ── Summary ───────────────────────────────────────────────────
section("SUMMARY  [deferred]")
empty_sum = [i for i in items if not i.get("summary")]
has_sum   = [i for i in items if i.get("summary")]
sum_lens  = [len(i["summary"]) for i in has_sum]
print(f"  Empty:   {len(empty_sum)}  ({pct(len(empty_sum), len(items))})")
print(f"  Present: {len(has_sum)}  ({pct(len(has_sum), len(items))})")
if sum_lens:
    print(f"  {count_stats(sum_lens, 'Items per summary  ')}")

both_missing = sum(1 for i in items if not i.get("description") and not i.get("summary"))
both_present = sum(1 for i in items if i.get("description") and i.get("summary"))
print(f"  Missing both: {both_missing}  ({pct(both_missing, len(items))})")
print(f"  Has both:     {both_present}  ({pct(both_present, len(items))})")

# ── Attributes (product level) ────────────────────────────────
section("ATTRIBUTES  (product level, variable only)")
no_attrs    = [i for i in variable if not i.get("attributes")]
multi_attrs = [i for i in variable if len(i.get("attributes", [])) > 1]
attr_name_counts = Counter(a["name"] for i in variable for a in i.get("attributes", []))
option_counts = [len(a["options"]) for i in variable for a in i.get("attributes", [])]
print(f"  Variable products with no attributes:  {len(no_attrs)}")
print(f"  Variable products with >1 attribute:   {len(multi_attrs)}")
if option_counts:
    print(f"  {count_stats(option_counts, 'Options per attribute  ')}")
print(f"\n  Top attribute names:")
for name, count in attr_name_counts.most_common(10):
    print(f"    {count:>4}x  {name}")

# ── Variations ────────────────────────────────────────────────
section("VARIATIONS")
var_counts = [len(i.get("variations", [])) for i in variable]
print(f"  Total across all variable products: {len(all_variations)}")
print(f"  {count_stats(var_counts, 'Per product  ')}")
print(f"  Distribution:")
bucket_dist(var_counts, [5, 10, 25, 50, 999], ["2-5", "6-10", "11-25", "26-50", "51+"])

# variation images
v_no_imgs       = [v for v in all_variations if not v.get("variationImages")]
v_img_counts    = [len(v.get("variationImages", [])) for v in all_variations]
print(f"\n  Variations with no image: {len(v_no_imgs)}  ({pct(len(v_no_imgs), len(all_variations))})")
print(f"  {count_stats(v_img_counts, 'Images per variation  ')}")

# variation attribute
v_no_attr    = [v for v in all_variations if not v.get("attribute")]
attr_opt_all = Counter(a["option"] for v in all_variations for a in v.get("attribute", []))
attr_name_all = Counter(a["name"] for v in all_variations for a in v.get("attribute", []))
print(f"\n  Variations with no attribute: {len(v_no_attr)}")
print(f"  Unique attribute names across all variations:")
for name, count in attr_name_all.most_common(10):
    print(f"    {count:>5}x  {name}")
print(f"  Unique options total: {len(attr_opt_all)}")

print()
