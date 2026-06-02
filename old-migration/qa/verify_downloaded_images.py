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

mapped_set = set(url_map.keys())

errors = []
ok = []

def check(name, passed, detail=""):
    (ok if passed else errors).append(f"{name}{': ' + detail if detail else ''}")

# Collect URLs by type
all_urls = set()
product_urls_by_sku = {}
var_urls_by_vsku = {}

for item in items:
    sku = item["sku"]
    purls = [img["src"] for img in item.get("images", []) if img.get("src")]
    product_urls_by_sku[sku] = purls
    all_urls.update(purls)
    for url in item.get("descriptionImgs", []):
        if url: all_urls.add(url)
    for ve in item.get("variations", []):
        var = ve.get("variation", {})
        vsku = var.get("sku", sku)
        vurls = [img["src"] for img in var.get("images", []) if img.get("src")]
        var_urls_by_vsku[vsku] = vurls
        all_urls.update(vurls)
        for url in var.get("descriptionImgs", []):
            if url: all_urls.add(url)

# ── 1. All URLs accounted for ─────────────────────────────────────────────────

in_map = all_urls & mapped_set
in_failed = all_urls & failed_set
unaccounted = all_urls - in_map - in_failed
check("All image URLs accounted for (in map or failed)", not unaccounted,
      f"{len(unaccounted)} unaccounted")

# ── 2. No URL in both map and failed ─────────────────────────────────────────

in_both = mapped_set & failed_set
check("No URL appears in both url_map and failed.json", not in_both,
      f"{len(in_both)} duplicates")

# ── 3. No extra URLs in map not referenced by any item ───────────────────────

extra = mapped_set - all_urls
check("No extra URLs in url_map absent from items", not extra,
      f"{len(extra)} extra")

# ── 4. No product has ALL its images failed (will have no images in DB) ───────

no_product_images = [
    sku for sku, urls in product_urls_by_sku.items()
    if urls and all(u in failed_set for u in urls)
]
check("No product has all product images failed", not no_product_images,
      f"{len(no_product_images)} affected: {no_product_images[:3]}")

# ── 5. Variations with ALL images failed (informational only) ────────────────

no_var_images = [
    vsku for vsku, urls in var_urls_by_vsku.items()
    if urls and all(u in failed_set for u in urls)
]
# Not a failure — frontend falls back to parent product images

# ── Report ────────────────────────────────────────────────────────────────────

print("=" * 60)
print("  DOWNLOADED IMAGES VERIFICATION")
print("=" * 60)
print(f"  URLs in items:           {len(all_urls)}")
print(f"  In url_map:              {len(in_map)}")
print(f"  In failed.json:          {len(in_failed)}")
print(f"  Unaccounted:             {len(unaccounted)}")
print(f"  Products with no images: {len(no_product_images)}")
print(f"  Variations with no images: {len(no_var_images)} (frontend falls back to product)")
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
print("  → Write a summary of these results in docs/downloaded-images/verify.md")
