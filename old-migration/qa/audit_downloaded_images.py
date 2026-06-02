import json
import os
from pathlib import Path

BASE = Path(__file__).parent.parent  # migration/
IMAGES_DIR = BASE / "images"

with open(BASE / "recategorized/categorized_items.json") as f:
    items = json.load(f)

with open(IMAGES_DIR / "url_map.json") as f:
    url_map = json.load(f)

failed_data = json.load(open(IMAGES_DIR / "failed.json")) if (IMAGES_DIR / "failed.json").exists() else {}
failed_urls = failed_data.get("failed_to_download", [])
failed_set = {e["src"] for e in failed_urls}
collisions = failed_data.get("collisions", [])

# ── File checks ───────────────────────────────────────────────────────────────

total_mapped = len(url_map)
files_on_disk = sum(1 for p in url_map.values() if os.path.exists(p))
files_missing = total_mapped - files_on_disk
zero_byte = [p for p in url_map.values() if os.path.exists(p) and os.path.getsize(p) == 0]

VALID_EXTS = {".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg"}
bad_ext = [p for p in url_map.values() if os.path.exists(p) and Path(p).suffix.lower() not in VALID_EXTS]

# ── Coverage by type ──────────────────────────────────────────────────────────

type_urls = {"product": set(), "variation": set(), "description": set(), "var_description": set()}
for item in items:
    for img in item.get("images", []):
        if img.get("src"): type_urls["product"].add(img["src"])
    for url in item.get("descriptionImgs", []):
        if url: type_urls["description"].add(url)
    for ve in item.get("variations", []):
        var = ve.get("variation", {})
        for img in var.get("images", []):
            if img.get("src"): type_urls["variation"].add(img["src"])
        for url in var.get("descriptionImgs", []):
            if url: type_urls["var_description"].add(url)

# ── Items with no downloadable images ─────────────────────────────────────────

no_images = []
for item in items:
    product_urls = [img["src"] for img in item.get("images", []) if img.get("src")]
    if product_urls and all(u in failed_set for u in product_urls):
        no_images.append(item["sku"])

print("=" * 60)
print("  DOWNLOADED IMAGES AUDIT")
print("=" * 60)
print(f"  Items:                 {len(items)}")
print(f"  URLs in url_map:       {total_mapped}")
print(f"  Files on disk:         {files_on_disk}")
print(f"  In map but missing:    {files_missing}")
print(f"  Zero-byte files:       {len(zero_byte)}")
print(f"  Invalid extensions:    {len(bad_ext)}")
print(f"  Failed downloads:      {len(failed_urls)}")
print(f"  Collisions:            {len(collisions)}")
print(f"  Items with no images:  {len(no_images)}")

print()
print("── COVERAGE BY TYPE ──")
for type_name, urls in type_urls.items():
    downloaded = len(urls & set(url_map.keys()))
    failed = len(urls & failed_set)
    print(f"  {type_name:<20} {downloaded:>5} downloaded  {failed:>4} failed  {len(urls):>5} total")

if files_missing:
    print()
    print("── MISSING FROM DISK (in map but file gone) ──")
    for url, path in url_map.items():
        if not os.path.exists(path):
            print(f"  {path}")

if zero_byte:
    print()
    print("── ZERO-BYTE FILES ──")
    for p in zero_byte:
        print(f"  {p}")

if bad_ext:
    print()
    print("── UNEXPECTED EXTENSIONS ──")
    for p in bad_ext:
        print(f"  {p}")

if no_images:
    print()
    print("── ITEMS WITH ALL PRODUCT IMAGES FAILED ──")
    for sku in no_images:
        print(f"  {sku}")

if failed_urls:
    print()
    print("── FAILED DOWNLOADS ──")
    for entry in failed_urls[:10]:
        print(f"  [{entry['sku']}] {entry['src']}")
    if len(failed_urls) > 10:
        print(f"  ... and {len(failed_urls) - 10} more (see migration/images/failed.json)")

if collisions:
    print()
    print("── COLLISIONS ──")
    for c in collisions:
        print(f"  existing: [{c['existing']['sku']}] {c['existing']['src']}")
        print(f"  tried:    [{c['tried']['sku']}] {c['tried']['src']}")
        print()

print()
print("  → Write a summary of these results in docs/downloaded-images/audit.md")
