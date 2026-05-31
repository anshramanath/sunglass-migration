import json
from pathlib import Path

BASE = Path(__file__).parent.parent  # migration/
IMAGES_DIR = BASE / "images"

with open(BASE / "recategorized/categorized_items.json") as f:
    items = json.load(f)

with open(IMAGES_DIR / "url_map.json") as f:
    url_map = json.load(f)

failed_data = json.load(open(IMAGES_DIR / "failed.json")) if (IMAGES_DIR / "failed.json").exists() else {}
failed_set = {e["src"] for e in failed_data.get("failed_to_download", [])}

# Collect all image URLs referenced in items
all_urls = set()
for item in items:
    for img in item.get("images", []):
        if img.get("src"):
            all_urls.add(img["src"])
    for url in item.get("descriptionImgs", []):
        if url:
            all_urls.add(url)
    for ve in item.get("variations", []):
        var = ve.get("variation", {})
        for img in var.get("images", []):
            if img.get("src"):
                all_urls.add(img["src"])
        for url in var.get("descriptionImgs", []):
            if url:
                all_urls.add(url)

in_map = all_urls & set(url_map.keys())
in_failed = all_urls & failed_set
unaccounted = all_urls - in_map - in_failed

errors = []
ok = []

def check(name, passed, detail=""):
    (ok if passed else errors).append(f"{name}{': ' + detail if detail else ''}")

check("All image URLs accounted for (in map or failed)", not unaccounted,
      f"{len(unaccounted)} unaccounted")
check("url_map has no URLs absent from items", not (set(url_map.keys()) - all_urls),
      f"{len(set(url_map.keys()) - all_urls)} extra URLs in map")

print("=" * 60)
print("  DOWNLOADED IMAGES VERIFICATION")
print("=" * 60)
print(f"  URLs in items:     {len(all_urls)}")
print(f"  In url_map:        {len(in_map)}")
print(f"  In failed.json:    {len(in_failed)}")
print(f"  Unaccounted:       {len(unaccounted)}")
print()

for name in ok:
    print(f"  ✓ {name}")
if errors:
    print()
    for e in errors:
        print(f"  ✗ {e}")
    if unaccounted:
        print()
        print("── UNACCOUNTED URLS ──")
        for url in sorted(unaccounted)[:10]:
            print(f"  {url}")
        if len(unaccounted) > 10:
            print(f"  ... and {len(unaccounted) - 10} more")
else:
    print("  ALL CHECKS PASSED")

print()
print("  → Update docs/downloaded-images/verify.md with these results.")
