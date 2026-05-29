import json
import re
from html import unescape

with open("products.json", "r", encoding="utf-8") as f:
    products = json.load(f)

with open("variations.json", "r", encoding="utf-8") as f:
    variations_by_parent = json.load(f)


def strip_html(html):
    if not html:
        return ""
    text = re.sub(r"<[^>]+>", " ", html)
    text = unescape(text)
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


def reshape_product(product, variation_stubs, full_variations_map):
    prices = product.get("prices") or {}
    regular_price = int(prices.get("regular_price") or 0)
    sale_price = int(prices.get("sale_price") or 0)
    sale = product.get("on_sale", False) and sale_price < regular_price

    # Flatten attribute term slugs
    attributes = []
    for attr in product.get("attributes", []):
        for term in attr.get("terms", []):
            slug = term.get("slug")
            if slug:
                attributes.append(slug)

    # Build variations array
    variations = []
    for stub in variation_stubs:
        stub_id = stub.get("id")
        stub_attrs = [a.get("value") for a in stub.get("attributes", []) if a.get("value")]

        full_var = full_variations_map.get(stub_id)
        if not full_var:
            continue

        variations.append({
            "attributes": stub_attrs,
            "variation": reshape_variation(full_var),
        })

    # Images
    images = [
        {"src": img.get("src"), "name": img.get("name") or ""}
        for img in product.get("images", [])
        if img.get("src")
    ]

    # Categories as flat slug array
    categories = [
        c.get("slug")
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
        "name": product.get("name"),
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


def reshape_variation(v):
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
        "name": v.get("name"),
        "slug": v.get("slug"),
        "sku": v.get("sku") or None,
        "variation": v.get("variation") or "",
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


clean_products = []
skipped = 0

for product in products:
    prices = product.get("prices") or {}
    regular_price = int(prices.get("regular_price") or 0)

    # Skip zero-price internal/service products
    if regular_price == 0:
        skipped += 1
        continue

    parent_id = str(product.get("id"))
    variation_stubs = product.get("variations", [])
    full_variations = variations_by_parent.get(parent_id, [])
    full_variations_map = {v["id"]: v for v in full_variations}

    clean_product = reshape_product(product, variation_stubs, full_variations_map)
    clean_products.append(clean_product)

with open("clean_products.json", "w", encoding="utf-8") as f:
    json.dump(clean_products, f, indent=2, ensure_ascii=False)

print(f"Skipped {skipped} zero-price products.")
print(f"Saved {len(clean_products)} clean products to clean_products.json")
