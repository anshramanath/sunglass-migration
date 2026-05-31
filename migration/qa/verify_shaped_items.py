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
    "invalid_weight":            BASE / "reshaped/invalid_weight_items.json",
    "multiple_variation_images": BASE / "reshaped/multiple_variation_images_items.json",
    "mismatched_attr":           BASE / "reshaped/mismatched_attr_items.json",
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

# ── 3. weight=0.0 not in shaped (goes to invalid_weight if unit is bad) ──────

zero_weight_in_shaped = [
    p["sku"] for p in reshaped["shaped"]
    if p.get("weight") == 0.0
]
check("weight=0.0 not in shaped bucket", not zero_weight_in_shaped,
      f"{zero_weight_in_shaped}")

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
    variations = p.get("variations", [])
    is_variable = bool(variations)
    min_p = p.get("minPriceCents", 0)
    max_p = p.get("maxPriceCents", 0)
    sale_p = p.get("salePriceCents")
    sale = p.get("sale", False)

    if not sku or " " in sku:
        shaped_violations.append(f"invalid sku: {sku}")
    if p.get("weight") is None or not p.get("weightUnit"):
        shaped_violations.append(f"invalid weight: {sku}")
    if not p.get("images"):
        shaped_violations.append(f"no images: {sku}")
    if not min_p:
        shaped_violations.append(f"zero min price: {sku}")

    if is_variable:
        var_prices = [ve["variation"].get("regularPriceCents", 0) for ve in variations]
        expected_min = min(var_prices) if var_prices else 0
        expected_max = max(var_prices) if var_prices else 0
        if min_p != expected_min:
            shaped_violations.append(f"minPriceCents {min_p} != variation min {expected_min}: {sku}")
        if max_p != expected_max:
            shaped_violations.append(f"maxPriceCents {max_p} != variation max {expected_max}: {sku}")
        if sale_p is not None:
            shaped_violations.append(f"variable product has non-null salePriceCents: {sku}")
        expected_sale = any(ve["variation"].get("sale", False) for ve in variations)
        if sale != expected_sale:
            shaped_violations.append(f"sale {sale} != expected {expected_sale} (from variations): {sku}")
    else:
        if min_p != max_p:
            shaped_violations.append(f"simple product min {min_p} != max {max_p}: {sku}")
        if sale_p is None:
            shaped_violations.append(f"simple product has null salePriceCents: {sku}")
        expected_sale = bool(sale_p and sale_p > 0 and sale_p < min_p)
        if sale != expected_sale:
            shaped_violations.append(f"sale {sale} != expected {expected_sale} (salePriceCents={sale_p} min={min_p}): {sku}")

    if any(len(ve.get("variation", {}).get("images", [])) > 1 for ve in variations):
        shaped_violations.append(f"variation >1 image: {sku}")

check("Shaped bucket passes all invariants (sku, weight, images, price)", not shaped_violations,
      f"{shaped_violations[:3]}")

# ── 8. All SKUs unique across all buckets ────────────────────────────────────

sku_counts = Counter(p["sku"] for p in all_items if p.get("sku"))
duplicate_skus = {s: c for s, c in sku_counts.items() if c > 1}
check("All SKUs unique across all buckets", not duplicate_skus,
      f"{len(duplicate_skus)} duplicates: {list(duplicate_skus)[:3]}")

# ── 9. Invalid SKU items correctly bucketed ───────────────────────────────────

invalid_in_shaped = [p["sku"] for p in reshaped["shaped"] if not p.get("sku") or " " in (p.get("sku") or "")]
check("No invalid SKUs in shaped bucket", not invalid_in_shaped, f"{invalid_in_shaped}")

# ── 10. Variation attributes consistent with product attributes ───────────────

attr_consistency_errors = []
for p in reshaped["shaped"]:
    sku = p.get("sku", "")
    variations = p.get("variations", [])
    attributes = p.get("attributes", [])

    if not variations:
        continue  # simple product

    power_slugs = {t["slug"] for a in attributes if a["name"] == "power" for t in a.get("terms", [])}
    non_power_attrs = [a for a in attributes if a["name"] != "power"]
    product_term_slugs = {term["slug"] for attr in non_power_attrs for term in attr.get("terms", [])}
    variation_slugs_used = {slug for ve in variations for slug in ve.get("attribute", []) if slug} - power_slugs

    # Product defines terms no variation uses (clicking that option finds nothing)
    extra_in_product = product_term_slugs - variation_slugs_used
    if extra_in_product:
        attr_consistency_errors.append(f"{sku}: product has terms unused by any variation: {sorted(extra_in_product)}")

    # Variation uses slugs not in product terms (orphaned variation)
    missing_from_product = variation_slugs_used - product_term_slugs
    if missing_from_product:
        attr_consistency_errors.append(f"{sku}: variation uses slugs not in product attrs: {sorted(missing_from_product)}")

    # Every slug in variation.attribute must exist in product attribute terms
    all_product_terms = {t["slug"] for a in attributes for t in a.get("terms", [])}
    for ve in variations:
        invalid = [s for s in ve.get("attribute", []) if s and s not in all_product_terms]
        if invalid:
            attr_consistency_errors.append(f"{sku}: variation slugs not in product terms: {invalid}")

check("Variation attributes consistent with product attributes", not attr_consistency_errors,
      f"{attr_consistency_errors[:3]}")

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
