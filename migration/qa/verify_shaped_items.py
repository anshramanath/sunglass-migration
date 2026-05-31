import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(line_buffering=True)

BASE = Path(__file__).parent.parent  # migration/

with open(BASE / "items/products.json") as f:
    raw_products = json.load(f)

BUCKETS = {
    "shaped":                    BASE / "reshaped/shaped_items.json",
    "zero_price":                BASE / "reshaped/zero_price_items.json",
    "invalid_sku":               BASE / "reshaped/invalid_sku_items.json",
    "missing_attributes":        BASE / "reshaped/missing_attributes_items.json",
    "no_image":                  BASE / "reshaped/no_image_items.json",
    "duplicate_name":            BASE / "reshaped/duplicate_name_items.json",
    "no_weight":                 BASE / "reshaped/no_weight_items.json",
    "multiple_variation_images": BASE / "reshaped/multiple_variation_images_items.json",
}

reshaped = {k: json.load(open(p)) for k, p in BUCKETS.items()}
all_items = [p for bucket in reshaped.values() for p in bucket]
by_slug = {p["slug"]: p for p in all_items}

errors = []
ok = []

def check(name, passed, detail=""):
    if passed:
        ok.append(name)
    else:
        errors.append(f"{name}{': ' + detail if detail else ''}")

# ── 1. All 647 products accounted for ────────────────────────────────────────

total = sum(len(v) for v in reshaped.values())
check("All products accounted for", total == len(raw_products),
      f"raw={len(raw_products)}, reshaped={total}")

raw_slugs = {p["slug"] for p in raw_products}
reshaped_slugs = {p["slug"] for p in all_items}
check("No products missing from output", raw_slugs == reshaped_slugs,
      f"{len(raw_slugs - reshaped_slugs)} missing")

# ── 2. Each product in exactly one bucket ────────────────────────────────────

from collections import Counter
slug_counts = Counter(p["slug"] for p in all_items)
dupes = {s: c for s, c in slug_counts.items() if c > 1}
check("No product in multiple buckets", not dupes,
      f"{len(dupes)} duplicates: {list(dupes)[:3]}")

# ── 3. weight=0.0 goes to no_weight, not shaped ──────────────────────────────

zero_weight_in_shaped = [
    p["sku"] for p in reshaped["shaped"]
    if p.get("weight") is not None and p.get("weight") == 0.0
]
check("weight=0.0 not in shaped bucket", not zero_weight_in_shaped,
      f"{zero_weight_in_shaped}")

zero_weight_in_no_weight = [
    p["sku"] for p in reshaped["no_weight"]
    if p.get("weight") == 0.0
]
check("weight=0.0 correctly in no_weight bucket", len(zero_weight_in_no_weight) >= 2,
      f"found {len(zero_weight_in_no_weight)} (expected at least 2)")

# ── 4. Power slugs normalized — no hyphen format (1-00, 2-50) ────────────────

HYPHEN_POWER = re.compile(r'^\d+-\d+$')
power_hyphens = []
for item in reshaped["shaped"]:
    for attr in item.get("attributes", []):
        if attr.get("name") == "power":
            for term in attr.get("terms", []):
                if HYPHEN_POWER.match(term.get("slug", "")):
                    power_hyphens.append((item["sku"], term["slug"]))
check("Power term slugs normalized (no hyphen format)", not power_hyphens,
      f"{power_hyphens[:3]}")

# ── 5. Categories are flat link arrays (WooCommerce URLs) ────────────────────

BASE_URL = "https://bikershades.com/product-category"
cat_structure_errors = []
for item in reshaped["shaped"]:
    for cat in item.get("categories", []):
        if not isinstance(cat, str) or not cat.startswith(BASE_URL):
            cat_structure_errors.append(item["sku"])
            break
check("Categories are flat WooCommerce link arrays", not cat_structure_errors,
      f"{len(cat_structure_errors)} items with wrong structure")

# ── 6. Attributes have {name, terms[{name, slug}]} structure ─────────────────

attr_structure_errors = []
for item in reshaped["shaped"]:
    for attr in item.get("attributes", []):
        if not isinstance(attr.get("name"), str):
            attr_structure_errors.append(item["sku"]); break
        for term in attr.get("terms", []):
            if not isinstance(term.get("name"), str) or not isinstance(term.get("slug"), str):
                attr_structure_errors.append(item["sku"]); break
check("Attributes have {name, terms[{name, slug}]} structure", not attr_structure_errors,
      f"{len(attr_structure_errors)} items with wrong structure")

# ── 7. Shaped bucket invariants ───────────────────────────────────────────────

shaped_violations = []
for p in reshaped["shaped"]:
    sku = p.get("sku", "")
    if not sku or " " in sku:
        shaped_violations.append(f"invalid sku: {sku}")
    if not p.get("weight") or p.get("weight") == 0.0:
        shaped_violations.append(f"missing/zero weight: {sku}")
    if not p.get("images"):
        shaped_violations.append(f"no images: {sku}")
    if not p.get("regularPriceInCents"):
        shaped_violations.append(f"zero price: {sku}")
    if any(len(ve.get("variation", {}).get("images", [])) > 1 for ve in p.get("variations", [])):
        shaped_violations.append(f"variation >1 image: {sku}")
check("Shaped bucket passes all invariants (sku, weight, images, price)", not shaped_violations,
      f"{shaped_violations[:3]}")

# ── 8. Invalid SKU items correctly bucketed ───────────────────────────────────

invalid_in_shaped = [p["sku"] for p in reshaped["shaped"] if not p.get("sku") or " " in (p.get("sku") or "")]
check("No invalid SKUs in shaped bucket", not invalid_in_shaped, f"{invalid_in_shaped}")

# ── Report ────────────────────────────────────────────────────────────────────

print("=" * 60)
print("  SHAPED ITEMS VERIFICATION")
print("=" * 60)
print(f"  Raw products:  {len(raw_products)}")
print(f"  Total reshaped: {total}")
print()
for name in ok:
    print(f"  ✓ {name}")
print()
if errors:
    print(f"  ✗ {len(errors)} check(s) failed:")
    for e in errors:
        print(f"    · {e}")
else:
    print("  ALL CHECKS PASSED")

print()
print("── BUCKET COUNTS ──")
for bucket, items in reshaped.items():
    print(f"  {bucket:<35} {len(items)}")
print(f"  {'TOTAL':<35} {total}")
