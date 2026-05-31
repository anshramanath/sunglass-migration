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


def get_filename(url, sku, used_filenames, collisions, url_to_filename):
    parsed = urlparse(url)
    path = parsed.path
    for prefix in ("/uploads/", "/gallery/"):
        if prefix in path:
            path = path.split(prefix, 1)[1]
            break
    base = path.lstrip("/").replace("/", "_") or "image"
    if parsed.query:
        stem, _, ext = base.rpartition(".")
        query = parsed.query.replace("=", "_").replace("&", "_")
        base = f"{stem}_{query}.{ext}" if stem else f"{base}_{query}"
    name = base
    if name in used_filenames:
        collisions.append({
            "existing": {"src": url_to_filename[name], "sku": url_to_sku.get(url_to_filename[name], "unknown")},
            "tried": {"src": url, "sku": sku},
        })
    used_filenames.add(name)
    url_to_filename[name] = url
    return name


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
    failed_urls = {e["src"]: e["sku"] for e in failed_data.get("failed_to_download", [])}
    collisions = failed_data.get("collisions", [])
else:
    failed_urls = {}
    collisions = []

url_to_sku = {}
for sku, url in collect_urls(items):
    if url not in url_to_sku:
        url_to_sku[url] = sku

all_urls = [url for url in url_to_sku if url not in url_map]

used_filenames = {Path(p).name for p in url_map.values()}
url_to_filename = {Path(p).name: url for url, p in url_map.items()}

total = downloaded = failed = 0

print(f"Downloading images for {len(items)} items...")
print(f"{len(url_to_sku)} unique URLs ({len(url_map)} already cached, {len(all_urls)} to download)\n")

for url in all_urls:
    total += 1
    sku = url_to_sku[url]
    local_path = str(LOCAL_DIR / get_filename(url, sku, used_filenames, collisions, url_to_filename))

    if download_image(url, local_path):
        url_map[url] = local_path
        failed_urls.pop(url, None)
        downloaded += 1
        with open(URL_MAP_PATH, "w") as f:
            json.dump(url_map, f, indent=2, ensure_ascii=False)
    else:
        failed_urls[url] = sku
        failed += 1

    seen = set()
    deduped_collisions = []
    for c in collisions:
        key = (c["existing"]["src"], c["tried"]["src"])
        if key not in seen:
            seen.add(key)
            deduped_collisions.append(c)

    with open(FAILED_PATH, "w") as f:
        json.dump({
            "failed_to_download": [{"sku": s, "src": u} for u, s in failed_urls.items()],
            "collisions": deduped_collisions,
        }, f, indent=2, ensure_ascii=False)

    time.sleep(0.05)

print(f"Done.")
print(f"  {downloaded} downloaded")
print(f"  {failed} failed → {FAILED_PATH}")
print(f"  {total} total")
print()
print("  → Run QA: python migration/qa/audit_downloaded_images.py")
print("  → Run QA: python migration/qa/verify_downloaded_images.py")
