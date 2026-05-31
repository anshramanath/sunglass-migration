import json
import os
import time
from urllib.parse import urlparse
from pathlib import Path
import requests

BASE = Path(__file__).parent.parent  # migration/
IMAGES_DIR = BASE / "images"
LOCAL_DIR = IMAGES_DIR / "local"
URL_MAP_PATH = IMAGES_DIR / "url_map.json"
SKIPPED_PATH = IMAGES_DIR / "skipped.json"


def get_filename(url, used_filenames):
    name = (urlparse(url).path.rstrip("/").split("/")[-1] or "image").split("?")[0]
    if name not in used_filenames:
        used_filenames.add(name)
        return name
    base, _, ext = name.rpartition(".")
    if not base:
        base, ext = name, ""
    i = 1
    while True:
        candidate = f"{base}_{i}.{ext}" if ext else f"{base}_{i}"
        if candidate not in used_filenames:
            used_filenames.add(candidate)
            print(f"  COLLISION {name} → {candidate}  ({url})")
            return candidate
        i += 1


def download_image(url, local_path):
    try:
        response = requests.get(url, timeout=30, stream=True)
        if response.status_code != 200:
            print(f"  SKIP {response.status_code}: {url}")
            return False
        with open(local_path, "wb") as f:
            for chunk in response.iter_content(8192):
                f.write(chunk)
        return True
    except Exception as e:
        print(f"  ERROR: {url} — {e}")
        return False


def collect_urls(items):
    for product in products:
        for img in product.get("images", []):
            if img.get("src"):
                yield img["src"]
        for url in product.get("descriptionImgs", []):
            if url:
                yield url
        for var_entry in product.get("variations", []):
            var = var_entry.get("variation", {})
            for img in var.get("images", []):
                if img.get("src"):
                    yield img["src"]
            for url in var.get("descriptionImgs", []):
                if url:
                    yield url


with open(BASE / "reshaped/clean_items.json") as f:
    products = json.load(f)

IMAGES_DIR.mkdir(exist_ok=True)
LOCAL_DIR.mkdir(exist_ok=True)

if URL_MAP_PATH.exists():
    with open(URL_MAP_PATH) as f:
        url_map = json.load(f)
else:
    url_map = {}

used_filenames = set(Path(p).name for p in url_map.values())

total = downloaded = skipped = failed = 0
skipped_urls = []

all_urls = list(dict.fromkeys(collect_urls(items)))  # dedupe, preserve order

print(f"Downloading images for {len(items)} clean products...\n")
print(f"{len(all_urls)} unique image URLs found\n")

for url in all_urls:
    total += 1

    if url in url_map and os.path.exists(url_map[url]):
        skipped += 1
        continue

    filename = get_filename(url, used_filenames)  # only reached for new URLs
    local_path = str(LOCAL_DIR / filename)

    if download_image(url, local_path):
        url_map[url] = local_path
        downloaded += 1
        with open(URL_MAP_PATH, "w") as f:
            json.dump(url_map, f, indent=2, ensure_ascii=False)
    else:
        skipped_urls.append(url)
        failed += 1

    time.sleep(0.05)

with open(SKIPPED_PATH, "w") as f:
    json.dump(skipped_urls, f, indent=2, ensure_ascii=False)

print(f"Done.")
print(f"  {downloaded} downloaded")
print(f"  {skipped} already cached")
print(f"  {failed} failed → {SKIPPED_PATH}")
print(f"  {total} total")
