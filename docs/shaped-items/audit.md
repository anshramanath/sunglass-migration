# Shaped Items Audit
_Last updated: 2026-05-31_

**Source:** `reshaped/shaped_items.json`
**Products:** 563 | **Variations:** 5,353

---

## Result

**Zero critical issues.** All required fields are present and valid across all 563 products and 5,353 variations.

---

## Critical Fields — All Pass

| Field | Status |
|-------|--------|
| `product.name/slug/sku/wpUrl/productUrl` | ✅ 563 / 563 |
| `product.minPriceCents` (> 0) | ✅ 563 / 563 |
| `product.maxPriceCents` (≥ minPriceCents) | ✅ 563 / 563 |
| `product.salePriceCents` (valid when sale=true, null for variable) | ✅ 563 / 563 |
| `product.stock` (0 or 1) | ✅ 563 / 563 |
| `product.weight` (not null) | ✅ 563 / 563 |
| `product.weightUnit` (valid, not N/A) | ✅ 563 / 563 |
| `variation.slug/sku/wpUrl/productUrl` | ✅ 5,353 / 5,353 |
| `variation.regularPriceCents` (> 0) | ✅ 5,353 / 5,353 |
| `variation.salePriceCents` (valid when sale=true) | ✅ 5,353 / 5,353 |
| `variation.stock` (0 or 1) | ✅ 5,353 / 5,353 |
| `variation.attribute` (not empty) | ✅ 5,353 / 5,353 |

---

## Informational — Empty Optional Fields

Expected gaps, not bugs.

| Field | Missing | Total | % | Notes |
|-------|--------:|------:|--:|-------|
| `product.summary` | 180 | 563 | 32.0% | WooCommerce short description was blank — frontend hides this section when empty |
| `product.attributes` | 114 | 563 | 20.2% | Simple products with no variation options — expected |
| `product.dimensions.length/width/height` | 41 | 563 | 7.3% | Not all products had dimensions in WooCommerce — all-or-nothing; partial dims are flagged to `invalid_dimensions_items` |
| `product.descriptionImgs` | 26 | 563 | 4.6% | No images embedded in description HTML — expected |
| `product.description` | 17 | 563 | 3.0% | No description text — expected |
| `variation.description` | 2,454 | 5,353 | 45.8% | Most variations have no description — frontend falls back to parent |
| `variation.images` | 3,460 | 5,353 | 64.6% | Variation images stripped if they duplicate a parent image — frontend falls back to product gallery |
| `variation.dimensions.length/width/height` | 179 | 5,353 | 3.3% | Variations without dimension data — expected |

---

## Notes

- `averageRating` and `reviewCount` are not present — dropped entirely. App builds its own review system.
- `product.attributes` empty (114 products) = simple products with no variation options. Correct — they have no `variations[]` either.
- Variable products have `salePriceCents = null` — price range is `minPriceCents`–`maxPriceCents` derived from variations.
- Simple products have `minPriceCents = maxPriceCents = regularPrice`.
- Product attribute terms are trimmed to only what variations actually use — unused terms stripped during reshape.
- `weightUnit` and `dimensionUnit` are derived from the last word of WooCommerce's `formatted_weight` / `formatted_dimensions` fields — not hardcoded. Products with a valid weight/dimensions but a missing or `N/A` unit are flagged to `missing_unit_items`.
- `product.dimensions` is all-or-nothing: all three of length/width/height must be present or none. Products with partial dimensions are flagged to `invalid_dimensions_items`. Products with no dimensions at all (41 products, 7.3%) are valid — dimensions are optional.
- `variation.images` empty (64.6%) is expected — variation images that duplicate a parent product image are stripped during reshape. Frontend falls back to product gallery for those variations.
- Variations no longer have `descriptionImgs` — description images belong to products only. The 4 variation description images that existed were duplicates of the parent's description image.
