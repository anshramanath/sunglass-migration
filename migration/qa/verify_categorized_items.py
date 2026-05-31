import json
import sys
from pathlib import Path

sys.stdout.reconfigure(line_buffering=True)

BASE = Path(__file__).parent.parent  # migration/

with open(BASE / "reshaped/shaped_items.json", encoding="utf-8") as f:
    shaped = json.load(f)

with open(BASE / "recategorized/categorized_items.json", encoding="utf-8") as f:
    categorized = json.load(f)

with open(BASE / "recategorized/no_category_items.json", encoding="utf-8") as f:
    no_cat = json.load(f)

with open(BASE / "recategorized/single_leaf_items.json", encoding="utf-8") as f:
    single_leaf = json.load(f)

issues = []

shaped_skus = {item["sku"] for item in shaped}
categorized_skus = {item["sku"] for item in categorized}
no_cat_skus = {item["sku"] for item in no_cat}
single_leaf_skus = {item["sku"] for item in single_leaf}

# ── 1. No items lost or duplicated ───────────────────────────────────────────

output_skus = categorized_skus | no_cat_skus | single_leaf_skus
missing = shaped_skus - output_skus
extra = output_skus - shaped_skus
overlap = categorized_skus & no_cat_skus

if missing:
    for sku in sorted(missing):
        issues.append(f"MISSING from both outputs: {sku}")

if extra:
    for sku in sorted(extra):
        issues.append(f"EXTRA in output (not in shaped): {sku}")

overlap = categorized_skus & no_cat_skus | categorized_skus & single_leaf_skus | no_cat_skus & single_leaf_skus
if overlap:
    for sku in sorted(overlap):
        issues.append(f"DUPLICATE: {sku} appears in multiple output buckets")

# ── 2. Count integrity ────────────────────────────────────────────────────────

expected_total = len(shaped)
actual_total = len(categorized) + len(no_cat) + len(single_leaf)
if expected_total != actual_total:
    issues.append(f"COUNT MISMATCH: shaped={expected_total}, categorized+no_cat={actual_total}")

# ── 3. Non-category fields unchanged ─────────────────────────────────────────

shaped_map = {item["sku"]: item for item in shaped}
for item in categorized:
    sku = item["sku"]
    original = shaped_map.get(sku)
    if not original:
        continue
    for field in ["name", "slug", "regularPriceInCents", "salePriceInCents", "sale", "inStock", "weight"]:
        if item.get(field) != original.get(field):
            issues.append(f"FIELD CHANGED during recategorize: {sku}.{field} — was {original.get(field)!r}, now {item.get(field)!r}")

# ── 4. No dropped slugs remain in categorized output ─────────────────────────

DROP_SLUGS = {
    "see-all-brands", "see-all-rx-frames", "see-all-eclipse-xt-frames",
    "see-all-try-before-you-buy", "all-products", "got-frames",
}

for item in categorized:
    sku = item["sku"]
    for path in item.get("categories", []):
        for node in path:
            if node.get("slug") in DROP_SLUGS:
                issues.append(f"DROP SLUG survived in output: {sku} — slug={node['slug']}")

# ── 5. No merged slugs remain in categorized output ──────────────────────────

MERGED_SLUGS = {"mirrored", "small-medium-shop-by-head-size", "low-nose-bridge-long-lashes-shades", "bifocal-type"}

for item in categorized:
    sku = item["sku"]
    for path in item.get("categories", []):
        for node in path:
            if node.get("slug") in MERGED_SLUGS:
                issues.append(f"MERGED SLUG survived in output: {sku} — slug={node['slug']}")

# ── Report ────────────────────────────────────────────────────────────────────

print("=" * 60)
print("  CATEGORIZED ITEMS VERIFICATION")
print("=" * 60)
print(f"  Shaped items:      {len(shaped)}")
print(f"  Categorized items: {len(categorized)}")
print(f"  No-category items: {len(no_cat)}")
print(f"  Single-leaf items: {len(single_leaf)}")
print(f"  Total accounted:   {len(categorized) + len(no_cat) + len(single_leaf)}")
print()

if not issues:
    print("  ✓ All checks passed")
else:
    print(f"  ✗ {len(issues)} issue(s) found:\n")
    for issue in issues:
        print(f"    · {issue}")
