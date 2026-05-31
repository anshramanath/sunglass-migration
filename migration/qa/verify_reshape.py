import json
import re
from collections import defaultdict
from pathlib import Path

BASE = Path(__file__).parent.parent  # migration/

# ── load raw data ─────────────────────────────────────────────────────────────

with open(BASE / "items/products.json") as f:
    raw_products = json.load(f)

with open(BASE / "items/variations/variations.json") as f:
    raw_variations_by_parent = json.load(f)

# ── load all reshaped buckets ─────────────────────────────────────────────────

BUCKETS = {
    "clean":                     BASE / "reshaped/clean_items.json",
    "zero_price":                BASE / "reshaped/zero_price_items.json",
    "invalid_sku":               BASE / "reshaped/invalid_sku_items.json",
    "missing_attributes":        BASE / "reshaped/missing_attributes_items.json",
    "no_image":                  BASE / "reshaped/no_image_items.json",
    "duplicate_name":            BASE / "reshaped/duplicate_name_items.json",
    "no_weight":                 BASE / "reshaped/no_weight_items.json",
    "multiple_variation_images": BASE / "reshaped/multiple_variation_images_items.json",
}

reshaped = {}
for bucket, path in BUCKETS.items():
    with open(path) as f:
        reshaped[bucket] = json.load(f)

all_reshaped = [p for bucket in reshaped.values() for p in bucket]
reshaped_by_slug = {p["slug"]: p for p in all_reshaped}

errors = []
warnings = []

def err(msg): errors.append(msg)
def warn(msg): warnings.append(msg)

def had(v):
    if v is None: return False
    if isinstance(v, str) and not v.strip(): return False
    if isinstance(v, list) and len(v) == 0: return False
    return True

def has(v):
    return had(v)

# ── SECTION 1: reshape integrity ──────────────────────────────────────────────

total_reshaped = sum(len(v) for v in reshaped.values())
if total_reshaped != len(raw_products):
    err(f"COUNT MISMATCH: raw={len(raw_products)}, reshaped={total_reshaped}")
else:
    print(f"✓ Count: all {len(raw_products)} products accounted for across buckets")

slug_counts = defaultdict(int)
for p in all_reshaped:
    slug_counts[p["slug"]] += 1
dupes = {s: c for s, c in slug_counts.items() if c > 1}
if dupes:
    err(f"DUPLICATE SLUGS across buckets: {dupes}")
else:
    print("✓ No duplicates: every product appears in exactly one bucket")

missing = [p["slug"] for p in raw_products if p["slug"] not in reshaped_by_slug]
if missing:
    err(f"MISSING FROM RESHAPED ({len(missing)}): {missing[:5]}")
else:
    print("✓ Coverage: every raw product present in reshaped output")

field_errors = 0
for raw in raw_products:
    slug = raw["slug"]
    r = reshaped_by_slug.get(slug)
    if not r:
        continue

    raw_name_core = raw.get("name", "").replace("&amp;", "&").strip()
    if r.get("name", "").lower() not in raw_name_core.lower() and raw_name_core.lower() not in r.get("name", "").lower():
        warn(f"Name drift: slug={slug} raw='{raw_name_core}' reshaped='{r.get('name')}'")

    if r.get("slug") != raw.get("slug"):
        err(f"Slug mismatch: {raw.get('slug')} → {r.get('slug')}")
        field_errors += 1

    if r.get("sku") != (raw.get("sku") or None):
        err(f"SKU mismatch: slug={slug} raw={raw.get('sku')} reshaped={r.get('sku')}")
        field_errors += 1

    raw_price = int((raw.get("prices") or {}).get("regular_price") or 0)
    if r.get("regularPriceInCents") != raw_price:
        err(f"Price mismatch: slug={slug} raw={raw_price} reshaped={r.get('regularPriceInCents')}")
        field_errors += 1

    if r.get("sale") and r.get("salePriceInCents", 0) >= r.get("regularPriceInCents", 0):
        err(f"Sale price >= regular price: slug={slug}")
        field_errors += 1

if field_errors == 0:
    print("✓ Field mapping: slug, SKU, price all match raw data")

var_count_errors = 0
for raw in raw_products:
    slug = raw["slug"]
    r = reshaped_by_slug.get(slug)
    if not r:
        continue
    raw_var_count = len(raw.get("variations", []))
    reshaped_var_count = len(r.get("variations", []))
    if reshaped_var_count != raw_var_count:
        full_vars = raw_variations_by_parent.get(str(raw.get("id")), [])
        warn(f"Variation count: slug={slug} raw={raw_var_count} reshaped={reshaped_var_count} fetched={len(full_vars)}")
        var_count_errors += 1

if var_count_errors == 0:
    print("✓ Variation counts: all products have correct number of variations")
else:
    print(f"⚠ Variation counts: {var_count_errors} mismatches (see warnings)")

var_field_errors = 0
for raw in raw_products:
    full_vars = raw_variations_by_parent.get(str(raw.get("id")), [])
    full_vars_by_slug = {v["slug"]: v for v in full_vars}
    r = reshaped_by_slug.get(raw["slug"])
    if not r:
        continue
    for ve in r.get("variations", []):
        v = ve.get("variation", {})
        rv = full_vars_by_slug.get(v.get("slug"))
        if not rv:
            continue
        if v.get("sku") != (rv.get("sku") or None):
            err(f"Variation SKU mismatch: parent={raw['slug']} vslug={v.get('slug')}")
            var_field_errors += 1
        raw_vprice = int((rv.get("prices") or {}).get("regular_price") or 0)
        if v.get("regularPriceInCents") != raw_vprice:
            err(f"Variation price mismatch: parent={raw['slug']} vslug={v.get('slug')}")
            var_field_errors += 1

if var_field_errors == 0:
    print("✓ Variation fields: SKU and price match raw data")

for p in reshaped["clean"]:
    if not p.get("sku") or " " in (p.get("sku") or ""):
        err(f"Clean bucket has invalid SKU: {p.get('sku')}")
    if not p.get("weight"):
        err(f"Clean bucket has missing/zero weight: {p.get('sku')}")
    if not p.get("images"):
        err(f"Clean bucket has no images: {p.get('sku')}")
    if any(len(ve.get("variation", {}).get("images", [])) > 1 for ve in p.get("variations", [])):
        err(f"Clean bucket has variation with >1 image: {p.get('sku')}")

print("✓ Bucket assignment: clean bucket passes all invariant checks")

# ── SECTION 2: data loss ──────────────────────────────────────────────────────

print()
print("── DATA LOSS CHECK ──")

losses = defaultdict(list)

for raw in raw_products:
    slug = raw["slug"]
    r = reshaped_by_slug.get(slug)
    if not r:
        continue

    prices = raw.get("prices") or {}

    for field, raw_val, reshaped_val in [
        ("name",               raw.get("name"),        r.get("name")),
        ("slug",               raw.get("slug"),         r.get("slug")),
        ("sku",                raw.get("sku"),          r.get("sku")),
        ("wpUrl",              raw.get("permalink"),    r.get("wpUrl")),
        ("regularPriceInCents",prices.get("regular_price"), r.get("regularPriceInCents")),
        ("summary",            raw.get("short_description"), r.get("summary")),
        ("categories",         raw.get("categories"),  r.get("categories")),
        ("images",             raw.get("images"),       r.get("images")),
        ("weight",             raw.get("weight"),       r.get("weight")),
    ]:
        if had(raw_val) and not has(reshaped_val):
            losses[field].append(slug)

    self_links = (raw.get("_links") or {}).get("self") or []
    raw_product_url = self_links[0].get("href") if self_links else None
    if had(raw_product_url) and not has(r.get("productUrl")):
        losses["productUrl"].append(slug)

    raw_desc_imgs = re.findall(r'<img[^>]+src=["\']([^"\']+)["\']', raw.get("description") or "")
    if had(raw_desc_imgs) and not has(r.get("descriptionImgs")):
        losses["descriptionImgs"].append(slug)

    raw_attrs = raw.get("attributes") or []
    if any(len(a.get("terms") or []) > 0 for a in raw_attrs) and not has(r.get("attributes")):
        losses["attributes"].append(slug)

    raw_dims = raw.get("dimensions") or {}
    for axis in ["length", "width", "height"]:
        if had(raw_dims.get(axis)) and not (r.get("dimensions") or {}).get(axis):
            losses[f"dimensions.{axis}"].append(slug)

    if had(raw.get("average_rating")) and float(raw.get("average_rating") or 0) > 0 and not r.get("averageRating"):
        losses["averageRating"].append(slug)

    if (raw.get("review_count") or 0) > 0 and not r.get("reviewCount"):
        losses["reviewCount"].append(slug)

    full_vars = raw_variations_by_parent.get(str(raw.get("id")), [])
    full_vars_by_slug = {v["slug"]: v for v in full_vars}

    for ve in r.get("variations", []):
        v = ve.get("variation", {})
        rv = full_vars_by_slug.get(v.get("slug"))
        if not rv:
            continue
        vprices = rv.get("prices") or {}
        for field, raw_val, reshaped_val in [
            ("variation.slug",               rv.get("slug"),                    v.get("slug")),
            ("variation.sku",                rv.get("sku"),                     v.get("sku")),
            ("variation.wpUrl",              rv.get("permalink"),               v.get("wpUrl")),
            ("variation.regularPriceInCents",vprices.get("regular_price"),      v.get("regularPriceInCents")),
            ("variation.weight",             rv.get("weight"),                  v.get("weight")),
        ]:
            if had(raw_val) and not has(reshaped_val):
                losses[field].append(v.get("slug"))

        rv_dims = rv.get("dimensions") or {}
        for axis in ["length", "width", "height"]:
            if had(rv_dims.get(axis)) and not (v.get("dimensions") or {}).get(axis):
                losses[f"variation.dimensions.{axis}"].append(v.get("slug"))

        if had(rv.get("images")) and not has(v.get("images")):
            losses["variation.images"].append(v.get("slug"))

if not losses:
    print("✓ No data loss detected across any field.")
else:
    for field, slugs in sorted(losses.items()):
        print(f"  ✗ {field}: {len(slugs)} affected")
        for s in slugs[:3]:
            print(f"      · {s}")
        if len(slugs) > 3:
            print(f"      ... and {len(slugs) - 3} more")

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
