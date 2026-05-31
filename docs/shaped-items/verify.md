# Shaped Items Verification
_Last updated: 2026-05-31_

**Source:** `reshaped/shaped_items.json` + all problem buckets
**Script:** `migration/qa/verify_shaped_items.py`

---

## Result

**All checks passed.** 647 raw products accounted for across all buckets.

---

## Checks

| Check | Result |
|-------|--------|
| All 647 products accounted for across buckets | ✅ |
| No product missing from output | ✅ |
| No product in multiple buckets | ✅ |
| `weight=0.0` not in shaped bucket | ✅ |
| `weight=0.0` correctly in no_weight bucket (at least 2) | ✅ |
| Power term slugs normalized — no hyphen format (`1-00`, `2-50`) | ✅ |
| Categories are flat WooCommerce link arrays | ✅ |
| Attributes have `{name, terms[{name, slug}]}` structure | ✅ |
| Shaped bucket passes all invariants (valid SKU, weight > 0, has images, price > 0, stock 0 or 1, no variation with >1 image) | ✅ |
| All SKUs unique across all buckets | ✅ |
| No invalid SKUs (null or containing space) in shaped bucket | ✅ |

---

## Bucket counts

| Bucket | Count |
|--------|------:|
| `shaped_items.json` | 586 |
| `zero_price_items.json` | 8 |
| `invalid_sku_items.json` | 22 |
| `missing_attributes_items.json` | 7 |
| `no_image_items.json` | 3 |
| `duplicate_name_items.json` | 6 |
| `no_weight_items.json` | 14 |
| `multiple_variation_images_items.json` | 1 |
| **Total** | **647** |
