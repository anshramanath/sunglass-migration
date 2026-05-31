import json
import os
from pathlib import Path

BASE = Path(__file__).parent.parent  # migration/
IMAGES_DIR = BASE / "images"

with open(IMAGES_DIR / "url_map.json") as f:
    url_map = json.load(f)

failed_data = json.load(open(IMAGES_DIR / "failed.json")) if (IMAGES_DIR / "failed.json").exists() else {}
failed_urls = failed_data.get("failed_to_download", [])
collisions = failed_data.get("collisions", [])

total_mapped = len(url_map)
files_on_disk = sum(1 for p in url_map.values() if os.path.exists(p))
files_missing = total_mapped - files_on_disk

print("=" * 60)
print("  DOWNLOADED IMAGES AUDIT")
print("=" * 60)
print(f"  URLs in url_map:       {total_mapped}")
print(f"  Files on disk:         {files_on_disk}")
print(f"  In map but missing:    {files_missing}")
print(f"  Failed downloads:      {len(failed_urls)}")
print(f"  Collisions:            {len(collisions)}")

if files_missing:
    print()
    print("── MISSING FILES (in map but not on disk) ──")
    for url, path in url_map.items():
        if not os.path.exists(path):
            print(f"  {path}")

if failed_urls:
    print()
    print("── FAILED DOWNLOADS ──")
    for entry in failed_urls[:10]:
        print(f"  [{entry['sku']}] {entry['src']}")
    if len(failed_urls) > 10:
        print(f"  ... and {len(failed_urls) - 10} more")

if collisions:
    print()
    print("── COLLISIONS ──")
    for c in collisions:
        print(f"  existing: [{c['existing']['sku']}] {c['existing']['src']}")
        print(f"  tried:    [{c['tried']['sku']}] {c['tried']['src']}")
        print()

print()
print("  → Update docs/downloaded-images/audit.md with these results.")
