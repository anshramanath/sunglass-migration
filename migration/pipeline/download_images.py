import json
import time
from urllib.parse import urlparse
from pathlib import Path
import requests

BASE = Path(__file__).parent.parent  # migration/
IMAGES_DIR = BASE / "images"
LOCAL_DIR = IMAGES_DIR / "local"
URL_MAP_PATH = IMAGES_DIR / "url_map.json"
FAILED_PATH = IMAGES_DIR / "failed.json"


def get_filename(url, sku, used_filenames, filename_to_sku, collisions):
    name = (urlparse(url).path.rstrip("/").split("/")[-1] or "image").split("?")[0]
    if name not in used_filenames:
        used_filenames.add(name)
        filename_to_sku[name] = sku
        return name
    base, _, ext = name.rpartition(".")
    if not base:
        base, ext = name, ""
    i = 1
    while True:
        candidate = f"{base}_{i}.{ext}" if ext else f"{base}_{i}"
        if candidate not in used_filenames:
            used_filenames.add(candidate)
            collisions.append({
                "existing": {"name": name, "sku": filename_to_sku.get(name, "unknown")},
                "tried": {"name": candidate, "sku": sku},
            })
            filename_to_sku[candidate] = sku
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
    for item in items:
        sku = item.get("sku", "unknown")
        for img in item.get("images", []):
            if img.get("src"):
                yield sku, img["src"]
        for url in item.get("descriptionImgs", []):
            if url:
                yield sku, url
        for var_entry in item.get("variations", []):
            var = var_entry.get("variation", {})
            vsku = var.get("sku") or sku
            for img in var.get("images", []):
                if img.get("src"):
                    yield vsku, img["src"]
            for url in var.get("descriptionImgs", []):
                if url:
                    yield vsku, url


with open(BASE / "recategorized/categorized_items.json") as f:
    items = json.load(f)

IMAGES_DIR.mkdir(exist_ok=True)
LOCAL_DIR.mkdir(exist_ok=True)

if URL_MAP_PATH.exists():
    with open(URL_MAP_PATH) as f:
        url_map = json.load(f)
else:
    url_map = {}

if FAILED_PATH.exists():
    with open(FAILED_PATH) as f:
        failed_data = json.load(f)
    failed_urls = set(failed_data.get("failed_to_download", []))
    collisions = failed_data.get("collisions", [])
else:
    failed_urls = set()
    collisions = []

# Build url → sku for all URLs (needed for collision reporting on cached files too)
url_to_sku = {}
for sku, url in collect_urls(items):
    if url not in url_to_sku:
        url_to_sku[url] = sku

# Filenames already claimed by cached downloads
used_filenames = set(Path(p).name for p in url_map.values())
filename_to_sku = {Path(local).name: url_to_sku.get(url, "unknown") for url, local in url_map.items()}

# URLs not yet downloaded, preserving first-seen order
all_urls = [url for url in url_to_sku if url not in url_map]

total = downloaded = failed = 0

print(f"Downloading images for {len(items)} items...")
print(f"{len(url_to_sku)} unique URLs ({len(url_map)} already cached, {len(all_urls)} to download)\n")

for url in all_urls:
    total += 1
    sku = url_to_sku[url]
    filename = get_filename(url, sku, used_filenames, filename_to_sku, collisions)
    local_path = str(LOCAL_DIR / filename)

    if download_image(url, local_path):
        url_map[url] = local_path
        failed_urls.discard(url)
        downloaded += 1
        with open(URL_MAP_PATH, "w") as f:
            json.dump(url_map, f, indent=2, ensure_ascii=False)
    else:
        failed_urls.add(url)
        failed += 1

    with open(FAILED_PATH, "w") as f:
        json.dump({"failed_to_download": sorted(failed_urls), "collisions": collisions}, f, indent=2, ensure_ascii=False)

    time.sleep(0.05)

print(f"Done.")
print(f"  {downloaded} downloaded")
print(f"  {failed} failed → {FAILED_PATH}")
print(f"  {total} total")
