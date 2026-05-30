import json
import os
import time
from urllib.parse import urlparse
from pathlib import Path
import requests

BASE = Path(__file__).parent.parent  # migration/
RESHAPED_DIR = str(BASE / "reshaped")
IMAGES_DIR = str(BASE / "images")

SHAPE_MAP = {
    "clean_products_shape.json": "clean-products",
    "zero_price_products_shape.json": "zero-price",
    "invalid_sku_products_shape.json": "invalid-sku",
    "missing_attributes_products_shape.json": "missing-attributes",
    "no_image_products_shape.json": "no-image",
    "duplicate_name_products_shape.json": "duplicate-name",
    "no_weight_products_shape.json": "no-weight",
}


def get_filename(url, used_in_folder):
    path = urlparse(url).path
    name = (path.rstrip("/").split("/")[-1] or "image").split("?")[0]

    if name not in used_in_folder:
        used_in_folder.add(name)
        return name

    base, _, ext = name.rpartition(".")
    if not base:
        base, ext = name, ""

    i = 1
    while True:
        candidate = f"{base}_{i}.{ext}" if ext else f"{base}_{i}"
        if candidate not in used_in_folder:
            used_in_folder.add(candidate)
            return candidate
        i += 1


def download_image(url, local_path):
    try:
        response = requests.get(url, timeout=30, stream=True)
        if response.status_code != 200:
            print(f"  SKIP {response.status_code}: {url}")
            return False
        os.makedirs(os.path.dirname(local_path), exist_ok=True)
        with open(local_path, "wb") as f:
            for chunk in response.iter_content(8192):
                f.write(chunk)
        return True
    except Exception as e:
        print(f"  ERROR: {url} — {e}")
        return False


def collect_images(product, shape_dir):
    sku = product.get("sku") or product.get("slug") or "unknown"
    used = {}

    def get_used(folder):
        if folder not in used:
            used[folder] = set(os.listdir(folder)) if os.path.exists(folder) else set()
        return used[folder]

    for img in product.get("images", []):
        url = img.get("src")
        if url:
            folder = os.path.join(shape_dir, "products", sku)
            yield url, os.path.join(folder, get_filename(url, get_used(folder)))

    for url in product.get("descriptionImgs", []):
        if url:
            folder = os.path.join(shape_dir, "descriptions", sku)
            yield url, os.path.join(folder, get_filename(url, get_used(folder)))

    for var_entry in product.get("variations", []):
        var = var_entry.get("variation", {})
        var_sku = var.get("sku") or var.get("slug") or "unknown"

        for img in var.get("images", []):
            url = img.get("src")
            if url:
                folder = os.path.join(shape_dir, "variations", var_sku)
                yield url, os.path.join(folder, get_filename(url, get_used(folder)))

        for url in var.get("descriptionImgs", []):
            if url:
                folder = os.path.join(shape_dir, "descriptions", sku)
                yield url, os.path.join(folder, get_filename(url, get_used(folder)))


all_skipped = {}

for shape_file, shape_name in SHAPE_MAP.items():
    shape_path = os.path.join(RESHAPED_DIR, shape_file)
    if not os.path.exists(shape_path):
        print(f"Skipping {shape_file} — not found.")
        continue

    with open(shape_path, "r", encoding="utf-8") as f:
        products = json.load(f)

    shape_dir = os.path.join(IMAGES_DIR, shape_name)
    url_map_path = os.path.join(shape_dir, "url_map.json")

    if os.path.exists(url_map_path):
        with open(url_map_path, "r", encoding="utf-8") as f:
            url_map = json.load(f)
    else:
        url_map = {}

    os.makedirs(shape_dir, exist_ok=True)

    print(f"\n--- {shape_name} ({len(products)} products) ---")

    total = downloaded = skipped = failed = 0
    shape_skipped = []

    for product in products:
        for url, local_path in collect_images(product, shape_dir):
            total += 1
            if url in url_map and os.path.exists(url_map[url]):
                skipped += 1
                continue

            if download_image(url, local_path):
                url_map[url] = local_path
                downloaded += 1
                with open(url_map_path, "w", encoding="utf-8") as f:
                    json.dump(url_map, f, indent=2, ensure_ascii=False)
            else:
                shape_skipped.append(url)
                failed += 1

            time.sleep(0.05)

    if shape_skipped:
        all_skipped[shape_name] = shape_skipped

    print(f"  {downloaded} downloaded, {skipped} already cached, {failed} failed, {total} total")

skipped_path = os.path.join(IMAGES_DIR, "skipped.json")
with open(skipped_path, "w", encoding="utf-8") as f:
    json.dump(all_skipped, f, indent=2, ensure_ascii=False)

total_failed = sum(len(v) for v in all_skipped.values())
print(f"\nDone. {total_failed} failed URLs written to {skipped_path}")
