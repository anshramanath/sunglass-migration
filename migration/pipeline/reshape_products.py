import json
import re
from html import unescape
from pathlib import Path

BASE = Path(__file__).parent.parent  # migration/
(BASE / "reshaped").mkdir(exist_ok=True)

with open(BASE / "products/products.json", "r", encoding="utf-8") as f:
    products = json.load(f)

with open(BASE / "products/variations/variations.json", "r", encoding="utf-8") as f:
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
    prices = product.get("prices") or {}
    regular_price = int(prices.get("regular_price") or 0)
    sale_price = int(prices.get("sale_price") or 0)
    sale = product.get("on_sale", False) and sale_price < regular_price

    # Group attributes by mapped name
    attributes_map = {}
    for attr in product.get("attributes", []):
        raw_name = attr.get("name", "")
        mapped = ATTRIBUTE_NAME_MAP.get(raw_name, slugify(raw_name))
        terms = [t.get("slug") for t in attr.get("terms", []) if t.get("slug")]
        if terms:
            if mapped in attributes_map:
                for t in terms:
                    if t not in attributes_map[mapped]:
                        attributes_map[mapped].append(t)
            else:
                attributes_map[mapped] = terms
    attributes = [{"name": k, "terms": v} for k, v in attributes_map.items()]

    # Build variations array
    variations = []
    for stub in variation_stubs:
        stub_id = stub.get("id")
        stub_attrs = stub.get("attributes", [])

        full_var = full_variations_map.get(stub_id)
        if not full_var:
            continue

        stub_values = [a.get("value") for a in stub_attrs if a.get("value")]

        variations.append({
            "attribute": stub_values,
            "variation": reshape_variation(full_var, stub_values),
        })

    # Images
    images = [
        {"src": img.get("src"), "name": img.get("name") or ""}
        for img in product.get("images", [])
        if img.get("src")
    ]

    # Categories as objects with all three fields
    categories = [
        {"name": c.get("name"), "slug": c.get("slug"), "link": c.get("link")}
        for c in product.get("categories", [])
        if c.get("slug")
    ]

    # Weight and dimensions
    weight_str = product.get("weight") or ""
    weight = float(weight_str) if weight_str else None

    dims = product.get("dimensions") or {}
    dimensions = {
        "length": float(dims.get("length")) if dims.get("length") else None,
        "width": float(dims.get("width")) if dims.get("width") else None,
        "height": float(dims.get("height")) if dims.get("height") else None,
    }

    links = product.get("_links") or {}
    self_links = links.get("self") or []
    product_url = self_links[0].get("href") if self_links else None

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
        "regularPriceInCents": regular_price,
        "salePriceInCents": sale_price,
        "averageRating": float(product.get("average_rating") or 0),
        "reviewCount": product.get("review_count") or 0,
        "inStock": product.get("is_in_stock", False),
        "categories": categories,
        "images": images,
        "attributes": attributes,
        "variations": variations,
        "weight": weight,
        "weightUnit": "oz",
        "dimensions": dimensions,
        "dimensionUnit": "in",
    }


def reshape_variation(v, stub_values=None):
    prices = v.get("prices") or {}
    regular_price = int(prices.get("regular_price") or 0)
    sale_price = int(prices.get("sale_price") or 0)
    sale = v.get("on_sale", False) and sale_price < regular_price

    links = v.get("_links") or {}
    self_links = links.get("self") or []
    product_url = self_links[0].get("href") if self_links else None

    images = [
        {"src": img.get("src"), "name": img.get("name") or ""}
        for img in v.get("images", [])
        if img.get("src")
    ]

    weight_str = v.get("weight") or ""
    weight = float(weight_str) if weight_str else None

    dims = v.get("dimensions") or {}
    dimensions = {
        "length": float(dims.get("length")) if dims.get("length") else None,
        "width": float(dims.get("width")) if dims.get("width") else None,
        "height": float(dims.get("height")) if dims.get("height") else None,
    }

    return {
        "slug": v.get("slug"),
        "sku": v.get("sku") or None,
        "variation": stub_values or [],
        "wpUrl": v.get("permalink"),
        "productUrl": product_url,
        "description": strip_html(v.get("description") or ""),
        "descriptionImgs": extract_description_images(v.get("description") or ""),
        "sale": sale,
        "regularPriceInCents": regular_price,
        "salePriceInCents": sale_price,
        "inStock": v.get("is_in_stock", False),
        "images": images,
        "weight": weight,
        "weightUnit": "oz",
        "dimensions": dimensions,
        "dimensionUnit": "in",
    }


def is_valid_sku(sku):
    return sku and " " not in sku


from collections import Counter

# Pre-compute duplicate cleaned names across all non-zero-price products
all_names = []
for product in products:
    prices = product.get("prices") or {}
    if int(prices.get("regular_price") or 0) > 0:
        all_names.append(clean_name(product.get("name", "")))
duplicate_names = {name for name, count in Counter(all_names).items() if count > 1}

clean_products = []
zero_price_products = []
invalid_sku_products = []
missing_attributes_products = []
no_image_products = []
duplicate_name_products = []
no_weight_products = []
multiple_variation_images_products = []

for product in products:
    prices = product.get("prices") or {}
    regular_price = int(prices.get("regular_price") or 0)

    if regular_price == 0:
        parent_id = str(product.get("id"))
        variation_stubs = product.get("variations", [])
        full_variations = variations_by_parent.get(parent_id, [])
        full_variations_map = {v["id"]: v for v in full_variations}
        zero_price_products.append(reshape_product(product, variation_stubs, full_variations_map))
        continue

    parent_id = str(product.get("id"))
    variation_stubs = product.get("variations", [])
    full_variations = variations_by_parent.get(parent_id, [])
    full_variations_map = {v["id"]: v for v in full_variations}

    clean_product = reshape_product(product, variation_stubs, full_variations_map)

    has_missing_attrs = any(
        not v.get("attribute") and not v.get("variation", {}).get("variation")
        for v in clean_product.get("variations", [])
    )

    has_multiple_variation_images = any(
        len(v.get("variation", {}).get("images", [])) > 1
        for v in clean_product.get("variations", [])
    )

    if not is_valid_sku(clean_product.get("sku")):
        invalid_sku_products.append(clean_product)
    elif has_missing_attrs:
        missing_attributes_products.append(clean_product)
    elif not clean_product.get("images"):
        no_image_products.append(clean_product)
    elif clean_product.get("name") in duplicate_names:
        duplicate_name_products.append(clean_product)
    elif not clean_product.get("weight"):
        no_weight_products.append(clean_product)
    elif has_multiple_variation_images:
        multiple_variation_images_products.append(clean_product)
    else:
        clean_products.append(clean_product)

with open(BASE / "reshaped/clean_products_shape.json", "w", encoding="utf-8") as f:
    json.dump(clean_products, f, indent=2, ensure_ascii=False)

with open(BASE / "reshaped/invalid_sku_products_shape.json", "w", encoding="utf-8") as f:
    json.dump(invalid_sku_products, f, indent=2, ensure_ascii=False)

with open(BASE / "reshaped/zero_price_products_shape.json", "w", encoding="utf-8") as f:
    json.dump(zero_price_products, f, indent=2, ensure_ascii=False)

with open(BASE / "reshaped/missing_attributes_products_shape.json", "w", encoding="utf-8") as f:
    json.dump(missing_attributes_products, f, indent=2, ensure_ascii=False)

with open(BASE / "reshaped/no_image_products_shape.json", "w", encoding="utf-8") as f:
    json.dump(no_image_products, f, indent=2, ensure_ascii=False)

with open(BASE / "reshaped/duplicate_name_products_shape.json", "w", encoding="utf-8") as f:
    json.dump(duplicate_name_products, f, indent=2, ensure_ascii=False)

with open(BASE / "reshaped/no_weight_products_shape.json", "w", encoding="utf-8") as f:
    json.dump(no_weight_products, f, indent=2, ensure_ascii=False)

with open(BASE / "reshaped/multiple_variation_images_products_shape.json", "w", encoding="utf-8") as f:
    json.dump(multiple_variation_images_products, f, indent=2, ensure_ascii=False)

print(f"Zero-price products: {len(zero_price_products)} → zero_price_products.json")
print(f"Invalid SKU products: {len(invalid_sku_products)} → invalid_sku_products.json")
print(f"Missing attributes products: {len(missing_attributes_products)} → missing_attributes_products.json")
print(f"No image products: {len(no_image_products)} → no_image_products.json")
print(f"Duplicate name products: {len(duplicate_name_products)} → duplicate_name_products.json")
print(f"No weight products: {len(no_weight_products)} → no_weight_products.json")
print(f"Multiple variation images products: {len(multiple_variation_images_products)} → multiple_variation_images_products.json")
print(f"Clean products: {len(clean_products)} → clean_products.json")
