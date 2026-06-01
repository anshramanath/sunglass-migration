# Shaped Items Verify
_Last updated: 2026-05-31_

**Source:** `items/products.json` cross-referenced against all reshaped buckets

---

## Result

**All checks passed.** All 647 raw products accounted for. No data loss, no duplicates, all invariants hold.

---

## Checks

| Check | Result |
|-------|--------|
| All 647 products accounted for across buckets | ✅ |
| No product missing from output | ✅ |
| No product in multiple buckets | ✅ |
| Power term slugs normalized — no hyphen format (`1-00`) | ✅ |
| Categories are flat WooCommerce link arrays | ✅ |
| Attributes have `{name, terms[{name, slug}]}` structure | ✅ |
| Shaped bucket passes all invariants (SKU, images, stock 0 or 1, no variation with >1 image, price min/max from variation regulars, variable salePriceCents null, variation/simple sale↔salePriceCents consistent) | ✅ |
| All SKUs unique across all buckets | ✅ |
| No invalid SKUs in shaped bucket | ✅ |
| Variation attributes consistent with product attributes | ✅ |

---

## Bucket Counts

| Bucket | Count |
|--------|------:|
| `shaped_items.json` | 578 |
| `zero_price_items.json` | 10 |
| `invalid_sku_items.json` | 22 |
| `missing_attributes_items.json` | 5 |
| `no_image_items.json` | 3 |
| `duplicate_name_items.json` | 6 |
| `multiple_variation_images_items.json` | 1 |
| `mismatched_attr_items.json` | 22 |
| **Total** | **647** |
