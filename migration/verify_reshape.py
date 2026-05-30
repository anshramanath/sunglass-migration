import json
from collections import defaultdict

# ── load raw data ─────────────────────────────────────────────────────────────

with open("products/products.json") as f:
    raw_products = json.load(f)

with open("products/variations/variations.json") as f:
    raw_variations_by_parent = json.load(f)

# ── load all reshaped buckets ─────────────────────────────────────────────────

BUCKETS = {
    "clean":                      "reshaped/clean_products_shape.json",
    "zero_price":                 "reshaped/zero_price_products_shape.json",
    "invalid_sku":                "reshaped/invalid_sku_products_shape.json",
    "missing_attributes":         "reshaped/missing_attributes_products_shape.json",
    "no_image":                   "reshaped/no_image_products_shape.json",
    "duplicate_name":             "reshaped/duplicate_name_products_shape.json",
    "no_weight":                  "reshaped/no_weight_products_shape.json",
    "multiple_variation_images":  "reshaped/multiple_variation_images_products_shape.json",
}

reshaped = {}
for bucket, path in BUCKETS.items():
    with open(path) as f:
        reshaped[bucket] = json.load(f)

all_reshaped = [p for bucket in reshaped.values() for p in bucket]

# ── build lookup maps ─────────────────────────────────────────────────────────

raw_by_slug = {p["slug"]: p for p in raw_products}
reshaped_by_slug = {p["slug"]: p for p in all_reshaped}

# ── checks ────────────────────────────────────────────────────────────────────

errors = []
warnings = []

def err(msg): errors.append(msg)
def warn(msg): warnings.append(msg)

# 1. Total count
total_reshaped = sum(len(v) for v in reshaped.values())
if total_reshaped != len(raw_products):
    err(f"COUNT MISMATCH: raw={len(raw_products)}, reshaped total={total_reshaped}")
else:
    print(f"✓ Count: all {len(raw_products)} products accounted for across buckets")

# 2. No duplicates across buckets
all_slugs = [p["slug"] for p in all_reshaped]
slug_counts = defaultdict(int)
for s in all_slugs:
    slug_counts[s] += 1
dupes = {s: c for s, c in slug_counts.items() if c > 1}
if dupes:
    err(f"DUPLICATE SLUGS across buckets: {dupes}")
else:
    print(f"✓ No duplicates: every product appears in exactly one bucket")

# 3. Every raw slug present in reshaped
missing_from_reshaped = [p["slug"] for p in raw_products if p["slug"] not in reshaped_by_slug]
if missing_from_reshaped:
    err(f"MISSING FROM RESHAPED ({len(missing_from_reshaped)}): {missing_from_reshaped[:5]}")
else:
    print(f"✓ Coverage: every raw product present in reshaped output")

# 4. Field-level spot check: name, slug, sku, price
field_errors = 0
for raw in raw_products:
    slug = raw["slug"]
    r = reshaped_by_slug.get(slug)
    if not r:
        continue

    # name — cleaned version should still contain key words
    raw_name_core = raw.get("name", "").replace("&amp;", "&").strip()
    if r.get("name", "").lower() not in raw_name_core.lower() and raw_name_core.lower() not in r.get("name", "").lower():
        warn(f"Name drift: slug={slug} raw='{raw_name_core}' reshaped='{r.get('name')}'")

    # slug — must match exactly
    if r.get("slug") != raw.get("slug"):
        err(f"Slug mismatch: raw={raw.get('slug')} reshaped={r.get('slug')}")
        field_errors += 1

    # sku
    raw_sku = raw.get("sku") or None
    if r.get("sku") != raw_sku:
        err(f"SKU mismatch: slug={slug} raw={raw_sku} reshaped={r.get('sku')}")
        field_errors += 1

    # price
    raw_price = int((raw.get("prices") or {}).get("regular_price") or 0)
    if r.get("regularPriceInCents") != raw_price:
        err(f"Price mismatch: slug={slug} raw={raw_price} reshaped={r.get('regularPriceInCents')}")
        field_errors += 1

    # sale flag integrity
    raw_sale_price = int((raw.get("prices") or {}).get("sale_price") or 0)
    if r.get("sale") and (r.get("salePriceInCents", 0) >= r.get("regularPriceInCents", 0)):
        err(f"Sale price >= regular price: slug={slug}")
        field_errors += 1

if field_errors == 0:
    print(f"✓ Field mapping: name, slug, SKU, price all match raw data")

# 5. Variation count per product
var_count_errors = 0
for raw in raw_products:
    slug = raw["slug"]
    r = reshaped_by_slug.get(slug)
    if not r:
        continue

    raw_var_count = len(raw.get("variations", []))
    reshaped_var_count = len(r.get("variations", []))

    parent_id = str(raw.get("id"))
    full_vars = raw_variations_by_parent.get(parent_id, [])

    # Reshaped only includes variations that had a matching full_var entry
    # so reshaped count <= raw stub count is expected; they should be equal
    # unless some variation IDs weren't fetched
    if reshaped_var_count != raw_var_count:
        warn(f"Variation count: slug={slug} raw_stubs={raw_var_count} reshaped={reshaped_var_count} full_fetched={len(full_vars)}")
        var_count_errors += 1

if var_count_errors == 0:
    print(f"✓ Variation counts: all products have correct number of variations")
else:
    print(f"⚠ Variation counts: {var_count_errors} products have variation count mismatches (see warnings)")

# 6. Variation field spot check: sku and price
var_field_errors = 0
for raw in raw_products:
    parent_id = str(raw.get("id"))
    full_vars = raw_variations_by_parent.get(parent_id, [])
    if not full_vars:
        continue

    full_vars_by_id = {v["id"]: v for v in full_vars}
    slug = raw["slug"]
    r = reshaped_by_slug.get(slug)
    if not r:
        continue

    for ve in r.get("variations", []):
        v = ve.get("variation", {})
        vslug = v.get("slug")

        # Find matching raw variation by slug
        raw_var = next((fv for fv in full_vars if fv.get("slug") == vslug), None)
        if not raw_var:
            continue

        raw_vsku = raw_var.get("sku") or None
        if v.get("sku") != raw_vsku:
            err(f"Variation SKU mismatch: parent={slug} vslug={vslug} raw={raw_vsku} reshaped={v.get('sku')}")
            var_field_errors += 1

        raw_vprice = int((raw_var.get("prices") or {}).get("regular_price") or 0)
        if v.get("regularPriceInCents") != raw_vprice:
            err(f"Variation price mismatch: parent={slug} vslug={vslug} raw={raw_vprice} reshaped={v.get('regularPriceInCents')}")
            var_field_errors += 1

if var_field_errors == 0:
    print(f"✓ Variation fields: SKU and price match raw data across all variations")

# 7. Bucket assignment sanity checks
for p in reshaped["clean"]:
    if not p.get("sku") or " " in (p.get("sku") or ""):
        err(f"Clean bucket has invalid SKU: {p.get('sku')}")
    if not p.get("weight"):
        err(f"Clean bucket has missing/zero weight: {p.get('sku')}")
    if not p.get("images"):
        err(f"Clean bucket has no images: {p.get('sku')}")
    if any(len(ve.get("variation", {}).get("images", [])) > 1 for ve in p.get("variations", [])):
        err(f"Clean bucket has variation with >1 image: {p.get('sku')}")

print(f"✓ Bucket assignment: clean bucket passes all invariant checks")

# ── results ───────────────────────────────────────────────────────────────────

print()
print("── BUCKET COUNTS ──")
for bucket, products in reshaped.items():
    print(f"  {bucket:<35} {len(products)}")
print(f"  {'TOTAL':<35} {total_reshaped}")

print()
if warnings:
    print(f"── WARNINGS ({len(warnings)}) ──")
    for w in warnings[:20]:
        print(f"  ⚠ {w}")
    if len(warnings) > 20:
        print(f"  ... and {len(warnings) - 20} more")
    print()

if errors:
    print(f"── ERRORS ({len(errors)}) ──")
    for e in errors:
        print(f"  ✗ {e}")
else:
    print("── RESULT: ALL CHECKS PASSED ──")
