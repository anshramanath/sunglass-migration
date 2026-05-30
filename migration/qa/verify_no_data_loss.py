import json
import re
from collections import defaultdict
from pathlib import Path

BASE = Path(__file__).parent.parent  # migration/

with open(BASE / "products/products.json") as f:
    raw_products = json.load(f)

with open(BASE / "products/variations/variations.json") as f:
    raw_variations_by_parent = json.load(f)

BUCKETS = [
    BASE / "reshaped/clean_products_shape.json",
    BASE / "reshaped/zero_price_products_shape.json",
    BASE / "reshaped/invalid_sku_products_shape.json",
    BASE / "reshaped/missing_attributes_products_shape.json",
    BASE / "reshaped/no_image_products_shape.json",
    BASE / "reshaped/duplicate_name_products_shape.json",
    BASE / "reshaped/no_weight_products_shape.json",
    BASE / "reshaped/multiple_variation_images_products_shape.json",
]

all_reshaped = []
for path in BUCKETS:
    with open(path) as f:
        all_reshaped.extend(json.load(f))

reshaped_by_slug = {p["slug"]: p for p in all_reshaped}

losses = defaultdict(list)  # field → list of slugs where data was lost

def had(raw_val):
    if raw_val is None: return False
    if isinstance(raw_val, str) and not raw_val.strip(): return False
    if isinstance(raw_val, list) and len(raw_val) == 0: return False
    return True

def has(reshaped_val):
    if reshaped_val is None: return False
    if isinstance(reshaped_val, str) and not reshaped_val.strip(): return False
    if isinstance(reshaped_val, list) and len(reshaped_val) == 0: return False
    return True

for raw in raw_products:
    slug = raw["slug"]
    r = reshaped_by_slug.get(slug)
    if not r:
        continue

    prices = raw.get("prices") or {}

    # name
    if had(raw.get("name")) and not has(r.get("name")):
        losses["name"].append(slug)

    # slug
    if had(raw.get("slug")) and not has(r.get("slug")):
        losses["slug"].append(slug)

    # sku
    if had(raw.get("sku")) and not has(r.get("sku")):
        losses["sku"].append(slug)

    # permalink → wpUrl
    if had(raw.get("permalink")) and not has(r.get("wpUrl")):
        losses["wpUrl"].append(slug)

    # _links.self.href → productUrl
    self_links = (raw.get("_links") or {}).get("self") or []
    raw_product_url = self_links[0].get("href") if self_links else None
    if had(raw_product_url) and not has(r.get("productUrl")):
        losses["productUrl"].append(slug)

    # description → description (plain text)
    if had(raw.get("description")) and not has(r.get("description")):
        losses["description"].append(slug)

    # description img tags → descriptionImgs
    raw_desc_imgs = re.findall(r'<img[^>]+src=["\']([^"\']+)["\']', raw.get("description") or "")
    if had(raw_desc_imgs) and not has(r.get("descriptionImgs")):
        losses["descriptionImgs"].append(slug)

    # short_description → summary
    if had(raw.get("short_description")) and not has(r.get("summary")):
        losses["summary"].append(slug)

    # prices → regularPriceInCents
    if had(prices.get("regular_price")) and not has(r.get("regularPriceInCents")):
        losses["regularPriceInCents"].append(slug)

    # average_rating → averageRating
    if had(raw.get("average_rating")) and float(raw.get("average_rating") or 0) > 0 and not r.get("averageRating"):
        losses["averageRating"].append(slug)

    # review_count → reviewCount
    if (raw.get("review_count") or 0) > 0 and not r.get("reviewCount"):
        losses["reviewCount"].append(slug)

    # categories
    if had(raw.get("categories")) and not has(r.get("categories")):
        losses["categories"].append(slug)

    # images
    if had(raw.get("images")) and not has(r.get("images")):
        losses["images"].append(slug)

    # attributes
    raw_attrs = raw.get("attributes") or []
    has_attr_terms = any(len(a.get("terms") or []) > 0 for a in raw_attrs)
    if has_attr_terms and not has(r.get("attributes")):
        losses["attributes"].append(slug)

    # weight
    if had(raw.get("weight")) and r.get("weight") is None:
        losses["weight"].append(slug)

    # dimensions
    raw_dims = raw.get("dimensions") or {}
    if had(raw_dims.get("length")) and not (r.get("dimensions") or {}).get("length"):
        losses["dimensions.length"].append(slug)
    if had(raw_dims.get("width")) and not (r.get("dimensions") or {}).get("width"):
        losses["dimensions.width"].append(slug)
    if had(raw_dims.get("height")) and not (r.get("dimensions") or {}).get("height"):
        losses["dimensions.height"].append(slug)

    # ── variations ────────────────────────────────────────────────────────────

    parent_id = str(raw.get("id"))
    full_vars = raw_variations_by_parent.get(parent_id, [])
    full_vars_by_slug = {v["slug"]: v for v in full_vars}

    for ve in r.get("variations", []):
        v = ve.get("variation", {})
        vslug = v.get("slug")
        rv = full_vars_by_slug.get(vslug)
        if not rv:
            continue

        vprices = rv.get("prices") or {}

        if had(rv.get("slug")) and not has(v.get("slug")):
            losses["variation.slug"].append(vslug)
        if had(rv.get("sku")) and not has(v.get("sku")):
            losses["variation.sku"].append(vslug)
        if had(rv.get("permalink")) and not has(v.get("wpUrl")):
            losses["variation.wpUrl"].append(vslug)
        if had(vprices.get("regular_price")) and not has(v.get("regularPriceInCents")):
            losses["variation.regularPriceInCents"].append(vslug)
        if had(rv.get("weight")) and v.get("weight") is None:
            losses["variation.weight"].append(vslug)

        rv_dims = rv.get("dimensions") or {}
        if had(rv_dims.get("length")) and not (v.get("dimensions") or {}).get("length"):
            losses["variation.dimensions.length"].append(vslug)
        if had(rv_dims.get("width")) and not (v.get("dimensions") or {}).get("width"):
            losses["variation.dimensions.width"].append(vslug)
        if had(rv_dims.get("height")) and not (v.get("dimensions") or {}).get("height"):
            losses["variation.dimensions.height"].append(vslug)

        # variation image
        raw_var_imgs = rv.get("images") or []
        if had(raw_var_imgs) and not has(v.get("images")):
            losses["variation.images"].append(vslug)

# ── report ────────────────────────────────────────────────────────────────────

print("DATA LOSS REPORT — if a field existed in raw, does it exist in reshaped?")
print(f"Checked {len(raw_products)} products\n")

if not losses:
    print("✓ No data loss detected across any field.")
else:
    for field, slugs in sorted(losses.items()):
        print(f"  ✗ {field}: {len(slugs)} products lost this field")
        for s in slugs[:3]:
            print(f"      · {s}")
        if len(slugs) > 3:
            print(f"      ... and {len(slugs) - 3} more")
