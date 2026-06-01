import json
import re
from html import unescape
from pathlib import Path

BASE = Path(__file__).parent.parent  # migration/
(BASE / "reshaped").mkdir(exist_ok=True)

with open(BASE / "items/products.json", "r", encoding="utf-8") as f:
    raw_products = json.load(f)

with open(BASE / "items/variations.json", "r", encoding="utf-8") as f:
    variations_by_parent = json.load(f)


def clean_name(name):
    if not name:
        return ""
    name = re.sub(r"<[^>]+>", "", name)
    name = unescape(name).strip()
    return name


def slugify(text):
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"\s+", "-", text)
    return text


def parse_variation_attributes(variation_string, stub_attrs):
    if variation_string:
        parts = variation_string.split(", ")
        result = []
        for part in parts:
            if ": " in part:
                value = part.split(": ", 1)[1]
                result.append(slugify(value))
        if result:
            return result
    return [a.get("value", "") for a in stub_attrs if a.get("value")]


def strip_html(html):
    if not html:
        return ""
    text = unescape(html)
    text = re.sub(r"<[^>]+>", " ", text, flags=re.DOTALL)
    text = re.sub(r"<[^>]*", " ", text)  # remove any remaining unclosed tags
    text = re.sub(r"\s+", " ", text).strip()
    return text


def extract_description_images(html):
    if not html:
        return []
    return re.findall(r'<img[^>]+src=["\']([^"\']+)["\']', html)


def parse_summary(html):
    if not html:
        return []

    # Try parsing <li> tags first
    items = re.findall(r"<li[^>]*>(.*?)</li>", html, re.DOTALL)

    if items:
        result = []
        for item in items:
            text = re.sub(r"<[^>]+>", " ", item)
            text = unescape(text)
            text = re.sub(r"\s+", " ", text).strip()
            if text:
                result.append(text)
        return result

    # Fallback: strip all HTML and return as single-item array
    text = re.sub(r"<[^>]+>", " ", html)
    text = unescape(text)
    text = re.sub(r"\s+", " ", text).strip()
    return [text] if text else []


ATTRIBUTE_NAME_MAP = {
    "Choose Color (REQUIRED)": "color",
    "Choose Color": "color",
    "Choose Power": "power",
    "Choose Transition Type": "transition-type",
    "Filter by Frame Color": "frame-color",
    "Choose Frame Color (Required)": "frame-color",
    "Choose Style Color": "style-color",
    "Choose Bandana Color": "bandana-color",
    "Filter by Size": "size",
    "Choose Size": "size",
    "Choose 7 Eye Style": "7-eye-style",
    "Filter by Brand": "brand",
    "Filter by Foam Type": "foam-type",
    "Shipping Option": "shipping",
    "Original Sunglass Purchase Price": "original-price",
    "Qty (packs of 3)": "quantity-packs-3",
    "LENS - GENUINE TRANSITIONS": "lens-genuine-transition",
}


def reshape_product(product, variation_stubs, full_variations_map):
    # Group attributes by mapped slug, carry name+slug for both attribute and terms
    attributes_map = {}
    for attr in product.get("attributes", []):
        raw_name = attr.get("name", "")
        mapped_slug = ATTRIBUTE_NAME_MAP.get(raw_name, slugify(raw_name))
        terms = []
        for t in attr.get("terms", []):
            if not t.get("slug"):
                continue
            slug = t["slug"]
            if mapped_slug == "power":
                slug = normalize_power_slug(slug)
            terms.append({"name": t.get("name", ""), "slug": slug})
        if terms:
            if mapped_slug in attributes_map:
                existing_slugs = {t["slug"] for t in attributes_map[mapped_slug]["terms"]}
                for t in terms:
                    if t["slug"] not in existing_slugs:
                        attributes_map[mapped_slug]["terms"].append(t)
            else:
                attributes_map[mapped_slug] = {"name": mapped_slug, "terms": terms}
    attributes = list(attributes_map.values())

    # Build variations array
    variations = []
    for stub in variation_stubs:
        stub_id = stub.get("id")
        stub_attrs = stub.get("attributes", [])

        full_var = full_variations_map.get(stub_id)
        if not full_var:
            continue

        stub_values = []
        for a in stub_attrs:
            val = a.get("value")
            if not val:
                continue
            attr_name = ATTRIBUTE_NAME_MAP.get(a.get("name", ""), slugify(a.get("name", "")))
            if attr_name == "power":
                val = normalize_power_slug(val)
            stub_values.append(val)

        variations.append({
            "attribute": stub_values,
            "variation": reshape_variation(full_var),
        })

    # Images
    images = [
        {"src": img.get("src"), "name": img.get("name") or ""}
        for img in product.get("images", [])
        if img.get("src")
    ]
    parent_srcs = {img["src"] for img in images}

    # Strip variation images that duplicate a parent image — frontend falls back anyway
    for ve in variations:
        ve["variation"]["images"] = [
            img for img in ve["variation"].get("images", [])
            if img.get("src") not in parent_srcs
        ]

    # Keep only link — name and slug derived during recategorization
    categories = [
        c.get("link")
        for c in product.get("categories", [])
        if c.get("link")
    ]

    # Weight and dimensions — parse units from formatted fields
    weight_str = product.get("weight") or ""
    raw_weight = float(weight_str) if weight_str else None
    fw = (product.get("formatted_weight") or "").strip()
    raw_weight_unit = fw.split()[-1] if fw else None
    if raw_weight and is_valid_unit(raw_weight_unit):
        weight, weight_unit = raw_weight, raw_weight_unit
    else:
        weight, weight_unit = None, None

    dims = product.get("dimensions") or {}
    raw_dims = {
        "length": float(dims.get("length")) if dims.get("length") else None,
        "width": float(dims.get("width")) if dims.get("width") else None,
        "height": float(dims.get("height")) if dims.get("height") else None,
    }
    fd = (product.get("formatted_dimensions") or "").strip()
    raw_dimension_unit = fd.split()[-1] if fd else None
    if all(v is not None for v in raw_dims.values()) and is_valid_unit(raw_dimension_unit):
        dimensions, dimension_unit = raw_dims, raw_dimension_unit
    else:
        dimensions, dimension_unit = {"length": None, "width": None, "height": None}, None

    links = product.get("_links") or {}
    self_links = links.get("self") or []
    product_url = self_links[0].get("href") if self_links else None

    # Price range — derived from variations for variable products, direct for simple
    if variations:
        var_prices = [ve["variation"]["regularPriceCents"] for ve in variations]
        min_price = min(var_prices)
        max_price = max(var_prices)
        sale_price = None
        sale = any(ve["variation"]["sale"] for ve in variations)
    else:
        prices = product.get("prices") or {}
        regular_price = int(prices.get("regular_price") or 0)
        raw_sale_price = int(prices.get("sale_price") or 0)
        min_price = regular_price
        max_price = regular_price
        sale = raw_sale_price > 0 and raw_sale_price < min_price
        sale_price = raw_sale_price if sale else None

    return {
        "name": clean_name(product.get("name")),
        "slug": product.get("slug"),
        "sku": product.get("sku") or None,
        "wpUrl": product.get("permalink"),
        "productUrl": product_url,
        "description": strip_html(product.get("description") or ""),
        "descriptionImgs": extract_description_images(product.get("description") or ""),
        "summary": parse_summary(product.get("short_description") or ""),
        "sale": sale,
        "minPriceCents": min_price,
        "maxPriceCents": max_price,
        "salePriceCents": sale_price,
        "stock": 1 if product.get("is_in_stock", False) else 0,
        "categories": categories,
        "images": images,
        "attributes": attributes,
        "variations": variations,
        "weight": weight,
        "weightUnit": weight_unit,
        "dimensions": dimensions,
        "dimensionUnit": dimension_unit,
    }


def reshape_variation(v):
    prices = v.get("prices") or {}
    regular_price = int(prices.get("regular_price") or 0)
    raw_sale_price = int(prices.get("sale_price") or 0)
    sale = raw_sale_price > 0 and raw_sale_price < regular_price
    sale_price = raw_sale_price if sale else None

    links = v.get("_links") or {}
    self_links = links.get("self") or []
    product_url = self_links[0].get("href") if self_links else None

    images = [
        {"src": img.get("src"), "name": img.get("name") or ""}
        for img in v.get("images", [])
        if img.get("src")
    ]

    weight_str = v.get("weight") or ""
    raw_weight = float(weight_str) if weight_str else None
    fw = (v.get("formatted_weight") or "").strip()
    raw_weight_unit = fw.split()[-1] if fw else None
    if raw_weight and is_valid_unit(raw_weight_unit):
        weight, weight_unit = raw_weight, raw_weight_unit
    else:
        weight, weight_unit = None, None

    dims = v.get("dimensions") or {}
    raw_dims = {
        "length": float(dims.get("length")) if dims.get("length") else None,
        "width": float(dims.get("width")) if dims.get("width") else None,
        "height": float(dims.get("height")) if dims.get("height") else None,
    }
    fd = (v.get("formatted_dimensions") or "").strip()
    raw_dimension_unit = fd.split()[-1] if fd else None
    if all(v is not None for v in raw_dims.values()) and is_valid_unit(raw_dimension_unit):
        dimensions, dimension_unit = raw_dims, raw_dimension_unit
    else:
        dimensions, dimension_unit = {"length": None, "width": None, "height": None}, None

    return {
        "slug": v.get("slug"),
        "sku": v.get("sku") or None,
        "wpUrl": v.get("permalink"),
        "productUrl": product_url,
        "description": strip_html(v.get("description") or ""),
        "sale": sale,
        "regularPriceCents": regular_price,
        "salePriceCents": sale_price,
        "stock": 1 if v.get("is_in_stock", False) else 0,
        "images": images,
        "weight": weight,
        "weightUnit": weight_unit,
        "dimensions": dimensions,
        "dimensionUnit": dimension_unit,
    }


def is_valid_sku(sku):
    return sku and " " not in sku


def is_valid_unit(unit):
    return bool(unit) and unit != "N/A"


def is_valid_measurement(v):
    return v is not None


def normalize_power_slug(slug):
    m = re.match(r'^(\d+)-(\d+)$', slug)
    if m:
        return '%s.%s' % (m.group(1), m.group(2))
    return slug


from collections import Counter

# Pre-compute duplicate cleaned names across all non-zero-price products
all_names = []
for product in raw_products:
    prices = product.get("prices") or {}
    if int(prices.get("regular_price") or 0) > 0:
        all_names.append(clean_name(product.get("name", "")))
duplicate_names = {name for name, count in Counter(all_names).items() if count > 1}

clean_items = []
zero_price_items = []
invalid_sku_items = []
duplicate_sku_items = []
missing_attributes_items = []
no_image_items = []
duplicate_name_items = []
mismatched_attr_items = []

for product in raw_products:
    prices = product.get("prices") or {}
    regular_price = int(prices.get("regular_price") or 0)

    if regular_price == 0:
        parent_id = str(product.get("id"))
        variation_stubs = product.get("variations", [])
        full_variations = variations_by_parent.get(parent_id, [])
        full_variations_map = {v["id"]: v for v in full_variations}
        zero_price_items.append(reshape_product(product, variation_stubs, full_variations_map))
        continue

    parent_id = str(product.get("id"))
    variation_stubs = product.get("variations", [])
    full_variations = variations_by_parent.get(parent_id, [])
    full_variations_map = {v["id"]: v for v in full_variations}

    clean_product = reshape_product(product, variation_stubs, full_variations_map)

    # Check: all variation attribute slugs exist in product terms
    all_product_terms = {t["slug"] for a in clean_product.get("attributes", []) for t in a.get("terms", [])}
    has_attr_mismatch = any(
        any(s not in all_product_terms for s in ve.get("attribute", []) if s)
        for ve in clean_product.get("variations", [])
    )

    # Step 3: if checks pass, remove product attribute terms unused by any variation
    if not has_attr_mismatch and clean_product.get("variations"):
        used_slugs = {s for ve in clean_product["variations"] for s in ve["attribute"] if s}
        clean_product["attributes"] = [
            {**a, "terms": [t for t in a["terms"] if t["slug"] in used_slugs]}
            for a in clean_product.get("attributes", [])
            if any(t["slug"] in used_slugs for t in a["terms"])
        ]

    has_missing_attrs = any(
        not ve.get("attribute")
        for ve in clean_product.get("variations", [])
    )

    if not is_valid_sku(clean_product.get("sku")):
        invalid_sku_items.append(clean_product)
    elif clean_product.get("minPriceCents", 0) == 0:
        zero_price_items.append(clean_product)
    elif has_missing_attrs:
        missing_attributes_items.append(clean_product)
    elif has_attr_mismatch:
        mismatched_attr_items.append(clean_product)
    elif not clean_product.get("images"):
        no_image_items.append(clean_product)
    elif clean_product.get("name") in duplicate_names:
        duplicate_name_items.append(clean_product)
    else:
        clean_items.append(clean_product)

# Post-processing: pull any product with a globally duplicate SKU into duplicate_sku_items.
# Walk every bucket, add SKUs to seen; if any SKU already claimed, move whole product out.
seen_skus = set()
all_buckets = [
    clean_items,
    zero_price_items,
    invalid_sku_items,
    missing_attributes_items,
    no_image_items,
    duplicate_name_items,
    mismatched_attr_items,
]
for bucket in all_buckets:
    keep = []
    for p in bucket:
        skus = [p["sku"]] if p.get("sku") else []
        for ve in p.get("variations", []):
            v_sku = ve.get("variation", {}).get("sku")
            if v_sku:
                skus.append(v_sku)
        unique = set(skus)
        if len(unique) < len(skus) or unique & seen_skus:
            duplicate_sku_items.append(p)
        else:
            seen_skus.update(unique)
            keep.append(p)
    bucket[:] = keep

with open(BASE / "reshaped/shaped_items.json", "w", encoding="utf-8") as f:
    json.dump(clean_items, f, indent=2, ensure_ascii=False)

with open(BASE / "reshaped/invalid_sku_items.json", "w", encoding="utf-8") as f:
    json.dump(invalid_sku_items, f, indent=2, ensure_ascii=False)

with open(BASE / "reshaped/duplicate_sku_items.json", "w", encoding="utf-8") as f:
    json.dump(duplicate_sku_items, f, indent=2, ensure_ascii=False)

with open(BASE / "reshaped/zero_price_items.json", "w", encoding="utf-8") as f:
    json.dump(zero_price_items, f, indent=2, ensure_ascii=False)

with open(BASE / "reshaped/missing_attributes_items.json", "w", encoding="utf-8") as f:
    json.dump(missing_attributes_items, f, indent=2, ensure_ascii=False)

with open(BASE / "reshaped/no_image_items.json", "w", encoding="utf-8") as f:
    json.dump(no_image_items, f, indent=2, ensure_ascii=False)

with open(BASE / "reshaped/duplicate_name_items.json", "w", encoding="utf-8") as f:
    json.dump(duplicate_name_items, f, indent=2, ensure_ascii=False)

with open(BASE / "reshaped/mismatched_attr_items.json", "w", encoding="utf-8") as f:
    json.dump(mismatched_attr_items, f, indent=2, ensure_ascii=False)

print(f"Zero-price items:              {len(zero_price_items)} → zero_price_items.json")
print(f"Invalid SKU items:             {len(invalid_sku_items)} → invalid_sku_items.json")
print(f"Duplicate SKU items:           {len(duplicate_sku_items)} → duplicate_sku_items.json")
print(f"Missing attributes items:      {len(missing_attributes_items)} → missing_attributes_items.json")
print(f"No image items:                {len(no_image_items)} → no_image_items.json")
print(f"Duplicate name items:          {len(duplicate_name_items)} → duplicate_name_items.json")
print(f"Mismatched attr items:         {len(mismatched_attr_items)} → mismatched_attr_items.json")
print(f"Shaped items:                  {len(clean_items)} → shaped_items.json")
print()
print("  → Run QA: python migration/qa/audit_shaped_items.py")
print("  → Run QA: python migration/qa/verify_shaped_items.py")
