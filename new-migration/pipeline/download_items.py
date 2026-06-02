import json
import os
import time
from pathlib import Path
from urllib.parse import urlparse
from dotenv import load_dotenv
import requests

BASE = Path(__file__).parent.parent
load_dotenv(dotenv_path=BASE.parent / ".env")

BRAND_CONFIG = {
    "proSPORT Sunglasses": {"slug": "prosport"},
}

brand_name = os.getenv("BRAND")
config = BRAND_CONFIG.get(brand_name)
if not config:
    raise SystemExit(f"Unknown BRAND={brand_name!r}. Add it to BRAND_CONFIG.")

slug = config["slug"]
data_dir = BASE / "data" / slug

in_path = data_dir / "categorize-items" / "items.json"
if not in_path.exists():
    raise SystemExit(f"Run prosport_categorize_items.py first. Not found: {in_path}")

items = json.loads(in_path.read_text())

IMAGES_DIR = data_dir / "download-items"
LOCAL_DIR  = IMAGES_DIR / "images"
URL_MAP_PATH  = IMAGES_DIR / "download_map.json"
FAILED_PATH   = IMAGES_DIR / "flagged.json"

IMAGES_DIR.mkdir(parents=True, exist_ok=True)
LOCAL_DIR.mkdir(exist_ok=True)

# ── Resume state ──────────────────────────────────────────────────────────────

url_map = json.loads(URL_MAP_PATH.read_text()) if URL_MAP_PATH.exists() else {}

if FAILED_PATH.exists():
    failed_data   = json.loads(FAILED_PATH.read_text())
    failed_urls   = {e["src"]: e["sku"] for e in failed_data.get("failed_to_download", [])}
    collisions    = failed_data.get("collisions", [])
else:
    failed_urls = {}
    collisions  = []

# ── Helpers ───────────────────────────────────────────────────────────────────

def collect_urls(items):
    for item in items:
        sku = item.get("sku", "unknown")
        for img in item.get("images", []):
            if img.get("src"):
                yield sku, img["src"]
        for img in item.get("descriptionImages", []):
            if img.get("src"):
                yield sku, img["src"]
        for v in item.get("variations", []):
            vsku = v.get("sku") or sku
            for img in v.get("images", []):
                if img.get("src"):
                    yield vsku, img["src"]


def get_filename(url, sku, used_filenames, collisions, url_to_filename):
    parsed = urlparse(url)
    path   = parsed.path
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
    if name in used_filenames and url_to_filename.get(name) != url:
        collisions.append({
            "existing": {"src": url_to_filename[name], "sku": url_to_sku.get(url_to_filename[name], "unknown")},
            "tried":    {"src": url, "sku": sku},
        })
    used_filenames.add(name)
    url_to_filename[name] = url
    return name


def download_image(url, local_path):
    try:
        r = requests.get(url, timeout=30, stream=True)
        if r.status_code != 200:
            print(f"  SKIP {r.status_code}: {url}")
            return False
        with open(local_path, "wb") as f:
            for chunk in r.iter_content(8192):
                f.write(chunk)
        return True
    except Exception as e:
        print(f"  ERROR: {url} — {e}")
        return False


def flush_failed():
    seen = set()
    deduped = []
    for c in collisions:
        key = (c["existing"]["src"], c["tried"]["src"])
        if key not in seen:
            seen.add(key)
            deduped.append(c)
    FAILED_PATH.write_text(json.dumps({
        "failed_to_download": [{"sku": s, "src": u} for u, s in failed_urls.items()],
        "collisions": deduped,
    }, indent=2, ensure_ascii=False))


# ── Collect ───────────────────────────────────────────────────────────────────

url_to_sku = {}
for sku, url in collect_urls(items):
    if url not in url_to_sku:
        url_to_sku[url] = sku

all_urls = [url for url in url_to_sku if url not in url_map]

used_filenames  = {Path(p).name for p in url_map.values()}
url_to_filename = {Path(p).name: url for url, p in url_map.items()}

print(f"Downloading images for {len(items)} items  ({brand_name})")
print(f"{len(url_to_sku)} unique URLs — {len(url_map)} already cached, {len(all_urls)} to download\n")

# ── Download ──────────────────────────────────────────────────────────────────

downloaded = failed = 0

for url in all_urls:
    sku        = url_to_sku[url]
    filename   = get_filename(url, sku, used_filenames, collisions, url_to_filename)
    local_path = str(LOCAL_DIR / filename)

    if download_image(url, local_path):
        url_map[url] = local_path
        failed_urls.pop(url, None)
        downloaded += 1
        URL_MAP_PATH.write_text(json.dumps(url_map, indent=2, ensure_ascii=False))
    else:
        failed_urls[url] = sku
        failed += 1

    flush_failed()
    time.sleep(0.05)

# ── Summary ───────────────────────────────────────────────────────────────────

print(f"Done.")
print(f"  {downloaded} downloaded")
print(f"  {len(url_map) - downloaded} skipped (already cached)")
print(f"  {failed} flagged → {FAILED_PATH}")
print(f"  download_map → {URL_MAP_PATH}  ({len(url_map)} entries)")
