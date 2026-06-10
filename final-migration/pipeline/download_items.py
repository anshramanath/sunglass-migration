import json
import sys
import time
from pathlib import Path
from urllib.parse import urlparse

import requests

sys.path.insert(0, str(Path(__file__).parent.parent))
from config import BASE, load_brand

brand_key, config = load_brand()
slug = config["slug"]

in_path = BASE / "data" / slug / "validate-items-final" / "items.json"
if not in_path.exists():
    raise SystemExit(f"Run validate_items_final.py first. Not found: {in_path}")


items = json.loads(in_path.read_text())

IMAGES_DIR   = BASE / "data" / slug / "download-items"
LOCAL_DIR    = IMAGES_DIR / "images"
MAP_PATH     = IMAGES_DIR / "download_map.json"
FAILED_PATH  = IMAGES_DIR / "flagged.json"

IMAGES_DIR.mkdir(parents=True, exist_ok=True)
LOCAL_DIR.mkdir(exist_ok=True)

url_map = json.loads(MAP_PATH.read_text()) if MAP_PATH.exists() else {}

if FAILED_PATH.exists():
    failed_data = json.loads(FAILED_PATH.read_text())
    failed_urls = {e["src"]: e["sku"] for e in failed_data.get("failed", [])}
else:
    failed_urls = {}


def collect_urls(items):
    for item in items:
        sku = item.get("sku") or item["slug"]
        for img in item.get("productImages") or []:
            yield sku, img["src"]
        for img in item.get("descriptionImages") or []:
            yield sku, img["src"]
        for v in item.get("variations") or []:
            vsku = v["sku"]
            for img in v.get("variationImages") or []:
                yield vsku, img["src"]


def make_filename(url, used, collisions, url_to_filename):
    parsed = urlparse(url)
    path = parsed.path
    for prefix in ("/uploads/", "/gallery/"):
        if prefix in path:
            path = path.split(prefix, 1)[1]
            break
    name = path.lstrip("/").replace("/", "_") or "image"
    if parsed.query:
        stem, _, ext = name.rpartition(".")
        q = parsed.query.replace("=", "_").replace("&", "_")
        name = f"{stem}_{q}.{ext}" if stem else f"{name}_{q}"
    if name in used and url_to_filename.get(name) != url:
        collisions.append({"existing": url_to_filename[name], "tried": url})
    used.add(name)
    url_to_filename[name] = url
    return name


def download(url, dest):
    try:
        r = requests.get(url, timeout=30, stream=True)
        if r.status_code != 200:
            print(f"  SKIP {r.status_code}: {url}")
            return False
        with open(dest, "wb") as f:
            for chunk in r.iter_content(8192):
                f.write(chunk)
        return True
    except Exception as e:
        print(f"  ERROR: {url} — {e}")
        return False


def flush():
    FAILED_PATH.write_text(json.dumps({
        "failed": [{"sku": s, "src": u} for u, s in failed_urls.items()],
        "collisions": collisions,
    }, indent=2, ensure_ascii=False))


url_to_sku: dict[str, str] = {}
for sku, url in collect_urls(items):
    if url not in url_to_sku:
        url_to_sku[url] = sku

pending = [u for u in url_to_sku if u not in url_map]
used_filenames: set[str] = {Path(p).name for p in url_map.values()}
url_to_filename: dict[str, str] = {Path(p).name: u for u, p in url_map.items()}
collisions: list[dict] = []

print(f"{len(url_to_sku)} unique URLs — {len(url_map)} cached, {len(pending)} to download")

downloaded = failed = 0

for url in pending:
    sku      = url_to_sku[url]
    filename = make_filename(url, used_filenames, collisions, url_to_filename)
    dest     = str(LOCAL_DIR / filename)

    if download(url, dest):
        url_map[url] = dest
        failed_urls.pop(url, None)
        downloaded += 1
        MAP_PATH.write_text(json.dumps(url_map, indent=2, ensure_ascii=False))
    else:
        failed_urls[url] = sku
        failed += 1

    flush()
    time.sleep(0.05)

print(f"Done. {downloaded} downloaded, {failed} failed, {len(url_map)} total in map")
