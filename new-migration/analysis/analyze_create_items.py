import json
import os
import statistics
from collections import Counter, defaultdict
from pathlib import Path
from dotenv import load_dotenv

BASE = Path(__file__).parent.parent
load_dotenv(dotenv_path=BASE.parent / ".env")

BRAND_CONFIG = {
    "proSPORT Sunglasses": {"slug": "prosport"},
}

brand_name = os.getenv("BRAND")
config = BRAND_CONFIG.get(brand_name)
if not config:
    raise SystemExit(f"Unknown BRAND={brand_name!r}. Add it to BRAND_CONFIG.")

slug = config["slug"]
data_dir = BASE / "data" / slug

items   = json.loads((data_dir / "create-items" / "items.json").read_text())
flagged = json.loads((data_dir / "create-items" / "flagged.json").read_text())

variables = [p for p in items if p["type"] == "variable"]
simples   = [p for p in items if p["type"] == "simple"]
all_vars  = [v for p in variables for v in p.get("variations", [])]

SEP  = "=" * 68
DASH = "─" * 68

def pct(n, total):
    return f"{n}/{total} ({100*n/total:.1f}%)" if total else "0/0 (—)"

def has(v):
    if v is None: return False
    if isinstance(v, (list, str)) and len(v) == 0: return False
    return True

def cents(c):
    return f"${c/100:.2f}" if c is not None else "null"

def hist(values, buckets):
    """print an ASCII bucket histogram"""
    lines = []
    for lo, hi, label in buckets:
        n = sum(1 for v in values if lo <= v < hi)
        bar = "█" * min(n, 50)
        lines.append(f"    {label:<14} {bar}  {n}")
    return "\n".join(lines)

def pstats(values):
    if not values:
        return "  (no data)"
    s = sorted(values)
    return (
        f"  min={s[0]}  p25={s[len(s)//4]}  median={s[len(s)//2]}"
        f"  p75={s[3*len(s)//4]}  max={s[-1]}  mean={statistics.mean(s):.1f}"
    )

# ─────────────────────────────────────────────────────────────────────────────
print(SEP)
print(f"  CREATE ITEMS — DEEP ANALYSIS   {brand_name}")
print(SEP)

print(f"\n  Items total : {len(items)}  (variable: {len(variables)}, simple: {len(simples)})")
print(f"  Flagged     : {len(flagged)}")
print(f"  Variations  : {len(all_vars)}")


# ══════════════════════════════════════════════════════════════════════════════
print(f"\n{DASH}")
print(f"  1. PRODUCT FIELD PRESENCE")
print(DASH)

PRODUCT_SCALAR_FIELDS = [
    "id", "name", "slug", "oldLink", "type",
    "description", "sku",
    "minPriceCents", "maxPriceCents", "salePriceCents",
    "sale", "featured", "totalSales",
    "stock", "weight",
]
PRODUCT_ARRAY_FIELDS = ["descriptionImages", "shortDescription", "categories", "images", "attributes", "variations"]

for field in PRODUCT_SCALAR_FIELDS:
    n = sum(1 for p in items if has(p.get(field)))
    null_n = len(items) - n
    print(f"  {field:<22} present={pct(n, len(items))}  null={null_n}")

for field in PRODUCT_ARRAY_FIELDS:
    n_non_empty = sum(1 for p in items if has(p.get(field)))
    n_empty     = sum(1 for p in items if isinstance(p.get(field), list) and len(p[field]) == 0)
    n_null      = sum(1 for p in items if p.get(field) is None)
    print(f"  {field:<22} non-empty={pct(n_non_empty, len(items))}  empty={n_empty}  null={n_null}")

# dimensions: always an object — inspect inner field presence
dim_all_null   = sum(1 for p in items if p.get("dimensions") and all(p["dimensions"].get(k) is None for k in ["length","width","height"]))
dim_some_set   = sum(1 for p in items if p.get("dimensions") and any(p["dimensions"].get(k) is not None for k in ["length","width","height"]))
dim_all_set    = sum(1 for p in items if p.get("dimensions") and all(p["dimensions"].get(k) is not None for k in ["length","width","height"]))
print(f"\n  dimensions object breakdown ({len(items)} products):")
print(f"    all fields null  : {dim_all_null}")
print(f"    some fields set  : {dim_some_set - dim_all_set}")
print(f"    all fields set   : {dim_all_set}")


# ══════════════════════════════════════════════════════════════════════════════
print(f"\n{DASH}")
print(f"  2. VARIATION FIELD PRESENCE")
print(DASH)

VARIATION_SCALAR_FIELDS = [
    "id", "parent_id", "name", "type", "oldLink",
    "description", "sku",
    "regularPriceCents", "salePriceCents", "sale",
    "stock", "weight", "image",
]

for field in VARIATION_SCALAR_FIELDS:
    n = sum(1 for v in all_vars if has(v.get(field)))
    null_n = len(all_vars) - n
    print(f"  {field:<22} present={pct(n, len(all_vars))}  null/false={null_n}")

vdim_all_null = sum(1 for v in all_vars if v.get("dimensions") and all(v["dimensions"].get(k) is None for k in ["length","width","height"]))
vdim_all_set  = sum(1 for v in all_vars if v.get("dimensions") and all(v["dimensions"].get(k) is not None for k in ["length","width","height"]))
print(f"\n  variation dimensions ({len(all_vars)} variations):")
print(f"    all fields null : {vdim_all_null}")
print(f"    all fields set  : {vdim_all_set}")
print(f"    some fields set : {len(all_vars) - vdim_all_null - vdim_all_set}")


# ══════════════════════════════════════════════════════════════════════════════
print(f"\n{DASH}")
print(f"  3. PRICING — PRODUCTS")
print(DASH)

var_min_prices = [p["minPriceCents"] for p in variables if p.get("minPriceCents") is not None]
var_max_prices = [p["maxPriceCents"] for p in variables if p.get("maxPriceCents") is not None]

print(f"  Variable products with minPriceCents set: {pct(len(var_min_prices), len(variables))}")
print(f"  minPriceCents stats (variable):")
print(pstats(var_min_prices))
print(f"  maxPriceCents stats (variable):")
print(pstats(var_max_prices))

flat_priced = sum(1 for p in variables if p.get("minPriceCents") == p.get("maxPriceCents") and p.get("minPriceCents") is not None)
tiered      = sum(1 for p in variables if p.get("minPriceCents") is not None and p.get("maxPriceCents") is not None and p["minPriceCents"] != p["maxPriceCents"])
print(f"\n  Flat pricing (min==max)  : {flat_priced} products")
print(f"  Tiered pricing (min<max) : {tiered} products")
if tiered:
    ranges = [(p["maxPriceCents"] - p["minPriceCents"]) for p in variables
              if p.get("minPriceCents") is not None and p.get("maxPriceCents") is not None and p["minPriceCents"] != p["maxPriceCents"]]
    print(f"    price range width stats (cents):")
    print(pstats(ranges))
    print(f"    widest-range products:")
    for p in sorted(variables, key=lambda x: (x.get("maxPriceCents") or 0) - (x.get("minPriceCents") or 0), reverse=True)[:5]:
        lo = p.get("minPriceCents"); hi = p.get("maxPriceCents")
        if lo and hi and lo != hi:
            print(f"      id={p['id']}  {cents(lo)}–{cents(hi)}  {p['name'][:45]}")

print(f"\n  Simple products:")
sp_prices = [p.get("minPriceCents") for p in simples if p.get("minPriceCents") is not None]
print(f"  minPriceCents stats:")
print(pstats(sp_prices))

print(f"\n  sale=True — products: {pct(sum(1 for p in items if p.get('sale')), len(items))}")
print(f"  sale=True — variable: {pct(sum(1 for p in variables if p.get('sale')), len(variables))}")
print(f"  sale=True — simple  : {pct(sum(1 for p in simples if p.get('sale')), len(simples))}")
print(f"  featured=True       : {sum(1 for p in items if p.get('featured'))}/{len(items)}")


# ══════════════════════════════════════════════════════════════════════════════
print(f"\n{DASH}")
print(f"  4. PRICING — VARIATIONS")
print(DASH)

v_reg  = [v["regularPriceCents"] for v in all_vars if v.get("regularPriceCents") is not None]
v_sale = [v["salePriceCents"]    for v in all_vars if v.get("salePriceCents") is not None]
print(f"  regularPriceCents set: {pct(len(v_reg), len(all_vars))}")
print(f"  regularPriceCents stats:")
print(pstats(v_reg))
print(f"\n  salePriceCents set  : {pct(len(v_sale), len(all_vars))}")
print(f"  salePriceCents stats:")
print(pstats(v_sale))

on_sale_vars  = [v for v in all_vars if v.get("sale")]
on_sale_with_price = [v for v in on_sale_vars if v.get("salePriceCents") is not None]
on_sale_no_price   = [v for v in on_sale_vars if v.get("salePriceCents") is None]
print(f"\n  sale=True variations         : {len(on_sale_vars)}")
print(f"    with salePriceCents        : {len(on_sale_with_price)}")
print(f"    missing salePriceCents     : {len(on_sale_no_price)}")
if on_sale_no_price:
    for v in on_sale_no_price[:5]:
        print(f"      id={v['id']} sku={v.get('sku')} parent={v.get('parent_id')}")

bad_sale = [v for v in all_vars if v.get("salePriceCents") is not None and v.get("regularPriceCents") is not None
            and v["salePriceCents"] >= v["regularPriceCents"]]
print(f"\n  Variations where salePriceCents >= regularPriceCents : {len(bad_sale)}")
if bad_sale:
    for v in bad_sale[:5]:
        print(f"    id={v['id']} reg={cents(v['regularPriceCents'])} sale={cents(v['salePriceCents'])}")

discounts = [round((1 - v["salePriceCents"] / v["regularPriceCents"]) * 100)
             for v in all_vars if v.get("salePriceCents") and v.get("regularPriceCents") and v["regularPriceCents"] > 0]
if discounts:
    print(f"\n  Sale discount % (when sale price set):")
    print(pstats(discounts))
    dc = Counter(discounts)
    print(f"  Top discount rates: {dc.most_common(5)}")

unique_reg_prices = sorted(set(v_reg))
print(f"\n  Distinct regularPriceCents values ({len(unique_reg_prices)}):")
price_freq = Counter(v_reg)
for price, count in sorted(price_freq.items(), key=lambda x: -x[1])[:10]:
    print(f"    {cents(price):>8}  {count:>5} variations")


# ══════════════════════════════════════════════════════════════════════════════
print(f"\n{DASH}")
print(f"  5. VARIATION COUNT DISTRIBUTION")
print(DASH)

vcounts = [len(p["variations"]) for p in variables]
print(f"  Stats:")
print(pstats(vcounts))
buckets = [
    (1,   6,   "  1–5  "),
    (6,   11,  "  6–10 "),
    (11,  21,  " 11–20 "),
    (21,  51,  " 21–50 "),
    (51,  101, " 51–100"),
]
print(f"\n  Distribution:")
print(hist(vcounts, buckets))

print(f"\n  Products with most variations:")
for p in sorted(variables, key=lambda x: len(x["variations"]), reverse=True)[:10]:
    print(f"    {len(p['variations']):>4} vars  id={p['id']}  {p['name'][:50]}")

print(f"\n  Products with fewest variations:")
for p in sorted(variables, key=lambda x: len(x["variations"]))[:5]:
    print(f"    {len(p['variations']):>4} vars  id={p['id']}  {p['name'][:50]}")


# ══════════════════════════════════════════════════════════════════════════════
print(f"\n{DASH}")
print(f"  6. STOCK")
print(DASH)

print(f"  Products:")
p_stock = [p.get("stock") for p in items if p.get("stock") is not None]
p_stock_null = sum(1 for p in items if p.get("stock") is None)
p_oos  = sum(1 for p in items if p.get("stock") == 0)
print(f"    null : {p_stock_null}")
print(f"    0    : {p_oos}  (out-of-stock)")
print(f"    1    : {sum(1 for p in items if p.get('stock') == 1)}")
print(f"    >1   : {sum(1 for p in items if isinstance(p.get('stock'), int) and p['stock'] > 1)}")
print(f"    total stock units: {sum(s for s in p_stock if isinstance(s, int))}")

print(f"\n  Variations:")
v_stock = [v.get("stock") for v in all_vars if v.get("stock") is not None]
v_stock_null = sum(1 for v in all_vars if v.get("stock") is None)
v_oos  = sum(1 for v in all_vars if v.get("stock") == 0)
print(f"    null      : {v_stock_null}")
print(f"    0         : {v_oos}  ({100*v_oos/len(all_vars):.1f}% out of stock)")
print(f"    1         : {sum(1 for v in all_vars if v.get('stock') == 1)}")
print(f"    >1        : {sum(1 for v in all_vars if isinstance(v.get('stock'), int) and v['stock'] > 1)}")
print(f"    >10       : {sum(1 for v in all_vars if isinstance(v.get('stock'), int) and v['stock'] > 10)}")
print(f"    total stock units: {sum(s for s in v_stock if isinstance(s, int))}")
print(f"    stats:")
print(pstats([s for s in v_stock if isinstance(s, int)]))

fully_oos = [p for p in variables if p["variations"] and all(v.get("stock") == 0 for v in p["variations"])]
partially_oos = [p for p in variables if p["variations"] and any(v.get("stock") == 0 for v in p["variations"]) and not all(v.get("stock") == 0 for v in p["variations"])]
print(f"\n  Variable products fully out of stock   : {len(fully_oos)}")
print(f"  Variable products partially out of stock: {len(partially_oos)}")
if fully_oos:
    for p in fully_oos[:5]:
        print(f"    id={p['id']}  {p['name'][:50]}")


# ══════════════════════════════════════════════════════════════════════════════
print(f"\n{DASH}")
print(f"  7. WEIGHT")
print(DASH)

p_weight_set  = sum(1 for p in items if p.get("weight") is not None)
p_weight_null = len(items) - p_weight_set
p_weight_vals = [p["weight"] for p in items if p.get("weight") is not None]
print(f"  Products with weight: {pct(p_weight_set, len(items))}")
if p_weight_vals:
    print(f"  Unique product weights: {sorted(set(p_weight_vals))}")

v_weight_set  = sum(1 for v in all_vars if v.get("weight") is not None)
v_weight_null = len(all_vars) - v_weight_set
v_weight_vals = [v["weight"] for v in all_vars if v.get("weight") is not None]
print(f"\n  Variations with weight: {pct(v_weight_set, len(all_vars))}")
if v_weight_vals:
    wc = Counter(v_weight_vals)
    print(f"  Weight distribution: {dict(sorted(wc.items()))}")


# ══════════════════════════════════════════════════════════════════════════════
print(f"\n{DASH}")
print(f"  8. IMAGES")
print(DASH)

image_counts = [len(p.get("images", [])) for p in items]
print(f"  Images per product:")
print(pstats(image_counts))
img_dist = Counter(image_counts)
print(f"  Distribution: {dict(sorted(img_dist.items()))}")

no_images = [p for p in items if not p.get("images")]
if no_images:
    print(f"\n  Products with 0 images ({len(no_images)}):")
    for p in no_images:
        print(f"    id={p['id']}  {p['name'][:50]}")

print(f"\n  Total unique product image URLs: {len({img['src'] for p in items for img in p.get('images', [])})}")

v_img_null    = sum(1 for v in all_vars if v.get("image") is None)
v_img_present = sum(1 for v in all_vars if v.get("image") is not None)
print(f"\n  Variation images:")
print(f"    null (deduped)  : {pct(v_img_null, len(all_vars))}")
print(f"    present (unique): {pct(v_img_present, len(all_vars))}")
print(f"    unique image URLs: {len({v['image']['src'] for v in all_vars if v.get('image')})}")

# per-product: how many unique variation images does each product have
unique_var_imgs_per_product = [
    sum(1 for v in p["variations"] if v.get("image"))
    for p in variables
]
print(f"\n  Unique variation images per variable product:")
print(pstats(unique_var_imgs_per_product))
zero_var_imgs = sum(1 for x in unique_var_imgs_per_product if x == 0)
print(f"    products where all variation images are null: {zero_var_imgs}")


# ══════════════════════════════════════════════════════════════════════════════
print(f"\n{DASH}")
print(f"  9. DESCRIPTION & SHORT DESCRIPTION")
print(DASH)

desc_text_and_imgs = sum(1 for p in items if has(p.get("description")) and has(p.get("descriptionImages")))
desc_text_only     = sum(1 for p in items if has(p.get("description")) and not has(p.get("descriptionImages")))
desc_imgs_only     = sum(1 for p in items if not has(p.get("description")) and has(p.get("descriptionImages")))
desc_neither       = sum(1 for p in items if not has(p.get("description")) and not has(p.get("descriptionImages")))
print(f"  description + descriptionImages : {desc_text_and_imgs}")
print(f"  description text only           : {desc_text_only}")
print(f"  descriptionImages only          : {desc_imgs_only}")
print(f"  neither                         : {desc_neither}")

desc_img_counts = [len(p["descriptionImages"]) for p in items if has(p.get("descriptionImages"))]
if desc_img_counts:
    print(f"\n  descriptionImages per product (when set):")
    print(f"  Distribution: {dict(sorted(Counter(desc_img_counts).items()))}")

short_desc_counts = [len(p["shortDescription"]) for p in items if has(p.get("shortDescription"))]
print(f"\n  Products with non-empty shortDescription: {pct(len(short_desc_counts), len(items))}")
if short_desc_counts:
    print(f"  Bullet count stats:")
    print(pstats(short_desc_counts))

v_desc_set = sum(1 for v in all_vars if has(v.get("description")))
print(f"\n  Variations with description: {pct(v_desc_set, len(all_vars))}")


# ══════════════════════════════════════════════════════════════════════════════
print(f"\n{DASH}")
print(f"  10. CATEGORIES")
print(DASH)

all_category_names = [cat["name"] for p in items for cat in p.get("categories", [])]
cat_counter = Counter(all_category_names)
print(f"  Unique categories: {len(cat_counter)}")
print(f"\n  Products per category:")
for name, count in cat_counter.most_common():
    print(f"    {name:<30} {count:>4} products")

no_cat = [p for p in items if not p.get("categories")]
uncat  = [p for p in items if any(c["name"] == "Uncategorized" for c in p.get("categories", []))]
only_uncat = [p for p in items if p.get("categories") and all(c["name"] == "Uncategorized" for c in p["categories"])]
print(f"\n  Products with 0 categories            : {len(no_cat)}")
print(f"  Products with 'Uncategorized' present  : {len(uncat)}")
print(f"  Products with ONLY 'Uncategorized'     : {len(only_uncat)}")
if only_uncat:
    for p in only_uncat:
        print(f"    id={p['id']}  {p['name'][:50]}")

cat_counts_per_product = [len(p.get("categories", [])) for p in items]
print(f"\n  Categories per product:")
print(pstats(cat_counts_per_product))


# ══════════════════════════════════════════════════════════════════════════════
print(f"\n{DASH}")
print(f"  11. ATTRIBUTES — PRODUCTS")
print(DASH)

attr_names = [a["name"] for p in items for a in p.get("attributes", [])]
attr_counter = Counter(attr_names)
print(f"  Unique attribute names: {len(attr_counter)}")
for name, count in attr_counter.most_common():
    opts = sorted({o for p in items for a in p.get("attributes", []) if a["name"] == name for o in a.get("options", [])})
    option_counts = [len(a["options"]) for p in items for a in p.get("attributes", []) if a["name"] == name]
    print(f"\n  [{name}]")
    print(f"    products        : {count}")
    print(f"    total options   : {len(opts)}")
    print(f"    options/product : min={min(option_counts)} max={max(option_counts)} avg={statistics.mean(option_counts):.1f}")
    if len(opts) <= 25:
        print(f"    all options     : {opts}")
    else:
        by_freq = Counter(o for p in items for a in p.get("attributes", []) if a["name"] == name for o in a.get("options", []))
        print(f"    top 20 options  : {[o for o, _ in by_freq.most_common(20)]}")

attr_counts_per_product = [len(p.get("attributes", [])) for p in items]
print(f"\n  Attributes per product:")
print(pstats(attr_counts_per_product))
print(f"  Distribution: {dict(sorted(Counter(attr_counts_per_product).items()))}")


# ══════════════════════════════════════════════════════════════════════════════
print(f"\n{DASH}")
print(f"  12. ATTRIBUTES — VARIATIONS")
print(DASH)

vattr_names = [a["name"] for v in all_vars for a in v.get("attributes", [])]
vattr_counter = Counter(vattr_names)
print(f"  Unique attribute names: {len(vattr_counter)}")
for name, count in vattr_counter.most_common():
    opts = sorted({a["option"] for v in all_vars for a in v.get("attributes", []) if a["name"] == name})
    print(f"\n  [{name}]")
    print(f"    variations   : {count}")
    print(f"    total options: {len(opts)}")
    if len(opts) <= 25:
        print(f"    all options  : {opts}")
    else:
        by_freq = Counter(a["option"] for v in all_vars for a in v.get("attributes", []) if a["name"] == name)
        print(f"    top 20       : {[o for o, _ in by_freq.most_common(20)]}")

vattr_counts_per_var = [len(v.get("attributes", [])) for v in all_vars]
print(f"\n  Attributes per variation:")
print(pstats(vattr_counts_per_var))
print(f"  Distribution: {dict(sorted(Counter(vattr_counts_per_var).items()))}")


# ══════════════════════════════════════════════════════════════════════════════
print(f"\n{DASH}")
print(f"  13. SKU ANALYSIS")
print(DASH)

product_skus = [p["sku"] for p in items if p.get("sku")]
var_skus     = [v["sku"] for v in all_vars if v.get("sku")]

print(f"  Products with SKU: {pct(len(product_skus), len(items))}")
print(f"  Variations with SKU: {pct(len(var_skus), len(all_vars))}")

sku_len_p = [len(s) for s in product_skus]
sku_len_v = [len(s) for s in var_skus]
print(f"\n  Product SKU length stats:")
print(pstats(sku_len_p))
print(f"\n  Variation SKU length stats:")
print(pstats(sku_len_v))

sku_set = set(product_skus)
overlap = [v["sku"] for v in all_vars if v.get("sku") in sku_set]
print(f"\n  Variation SKUs that collide with a product SKU: {len(overlap)}")

all_skus = product_skus + var_skus
sku_dupes = [sku for sku, cnt in Counter(all_skus).items() if cnt > 1]
print(f"  Duplicate SKUs across all items+variations: {len(sku_dupes)}")
if sku_dupes:
    for sku in sku_dupes[:5]:
        print(f"    {sku}")


# ══════════════════════════════════════════════════════════════════════════════
print(f"\n{DASH}")
print(f"  14. TOTAL SALES")
print(DASH)

ts = [p.get("totalSales") for p in items if p.get("totalSales") is not None]
ts_null = sum(1 for p in items if p.get("totalSales") is None)
print(f"  totalSales present: {pct(len(ts), len(items))}")
print(f"  Stats:")
print(pstats(ts))
ts_zero = sum(1 for t in ts if t == 0)
print(f"  Products with 0 sales : {ts_zero}")
print(f"  Products with >100 sales: {sum(1 for t in ts if t > 100)}")
print(f"  Total sales across all items: {sum(ts)}")

print(f"\n  Top 10 by totalSales:")
for p in sorted(items, key=lambda x: x.get("totalSales") or 0, reverse=True)[:10]:
    print(f"    {p.get('totalSales'):>5}  id={p['id']}  {p['name'][:50]}")


# ══════════════════════════════════════════════════════════════════════════════
print(f"\n{DASH}")
print(f"  15. DATA QUALITY SIGNALS")
print(DASH)

# Products missing both description and shortDescription
bare_products = [p for p in items if not has(p.get("description")) and not has(p.get("shortDescription")) and not has(p.get("descriptionImages"))]
print(f"  Products with no description, shortDescription, or descriptionImages: {len(bare_products)}")
if bare_products:
    for p in bare_products[:10]:
        print(f"    id={p['id']}  {p['name'][:50]}")

# Variable products with sale=True but not a single variation with salePriceCents
mismatch_sale = [
    p for p in variables
    if p.get("sale") and not any(v.get("salePriceCents") is not None for v in p["variations"])
]
print(f"\n  Variable products: sale=True but no variation has salePriceCents: {len(mismatch_sale)}")
if mismatch_sale:
    for p in mismatch_sale:
        print(f"    id={p['id']}  {p['name'][:50]}")

# Products with sale=True but minPriceCents == maxPriceCents (all variations same price)
flat_sale = [p for p in variables if p.get("sale") and p.get("minPriceCents") == p.get("maxPriceCents") and p.get("minPriceCents") is not None]
print(f"\n  Variable products: sale=True and flat price (all variations same regularPriceCents): {len(flat_sale)}")

# Variations with weight=0
v_zero_weight = sum(1 for v in all_vars if v.get("weight") == 0.0)
print(f"\n  Variations with weight=0.0: {v_zero_weight} (likely real 0 from WC, not missing)")

# Products where parent stock != sum of variation stocks (sanity — not an error, just interesting)
stock_mismatch = []
for p in variables:
    p_stock = p.get("stock")
    v_total = sum(v.get("stock") or 0 for v in p["variations"])
    if p_stock is not None and p_stock != v_total:
        stock_mismatch.append((p["id"], p["name"], p_stock, v_total))
print(f"\n  Products where product.stock != sum(variation.stock): {len(stock_mismatch)}")
print(f"  (expected — product.stock is the WC aggregate, variations are the source of truth)")
if stock_mismatch[:3]:
    for pid, name, ps, vs in stock_mismatch[:3]:
        print(f"    id={pid}  product.stock={ps}  sum(variations)={vs}  {name[:40]}")

# Variation attribute count != product attribute count
attr_count_mismatch = []
for p in variables:
    p_attr_names = {a["name"] for a in p.get("attributes", [])}
    for v in p["variations"]:
        v_attr_names = {a["name"] for a in v.get("attributes", [])}
        if v_attr_names != p_attr_names:
            attr_count_mismatch.append((p["id"], v["id"], p_attr_names, v_attr_names))

print(f"\n  Variations whose attribute names don't exactly match parent attribute names: {len(attr_count_mismatch)}")
if attr_count_mismatch:
    shown = set()
    for pid, vid, p_set, v_set in attr_count_mismatch[:10]:
        key = (pid, frozenset(p_set), frozenset(v_set))
        if key not in shown:
            shown.add(key)
            print(f"    product id={pid}  parent_attrs={sorted(p_set)}  var_attrs={sorted(v_set)}")


# ══════════════════════════════════════════════════════════════════════════════
print(f"\n{DASH}")
print(f"  16. FLAGGED PRODUCTS")
print(DASH)

print(f"  Count: {len(flagged)}")
for entry in flagged:
    p = entry["product"]
    print(f"\n  id={p['id']}  {p['name']}")
    for r in entry["reasons"]:
        print(f"    · {r}")
    vcount = len(p.get("variations", []))
    print(f"    · variations embedded: {vcount}")
    print(f"    · categories: {[c['name'] for c in p.get('categories', [])]}")

print(f"\n{SEP}")
print(f"  END OF ANALYSIS")
print(SEP)
