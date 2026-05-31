# Shaped Items Audit
_Last updated: 2026-05-31_

**Source:** `reshaped/shaped_items.json`
**Products:** 564 | **Variations:** 5,364

---

## Result

**Zero critical issues.** All required fields are present and valid across all 564 products and 5,364 variations.

---

## Critical Fields — All Pass

| Field | Status |
|-------|--------|
| `product.name/slug/sku/wpUrl/productUrl` | ✅ 564 / 564 |
| `product.minPriceCents` (> 0) | ✅ 564 / 564 |
| `product.maxPriceCents` (≥ minPriceCents) | ✅ 564 / 564 |
| `product.salePriceCents` (valid when sale=true, null for variable) | ✅ 564 / 564 |
| `product.stock` (0 or 1) | ✅ 564 / 564 |
| `product.weight` (not null, > 0) | ✅ 564 / 564 |
| `variation.slug/sku/wpUrl/productUrl` | ✅ 5,364 / 5,364 |
| `variation.regularPriceCents` (> 0) | ✅ 5,364 / 5,364 |
| `variation.salePriceCents` (valid when sale=true) | ✅ 5,364 / 5,364 |
| `variation.stock` (0 or 1) | ✅ 5,364 / 5,364 |
| `variation.attribute` (not empty) | ✅ 5,364 / 5,364 |

---

## Informational — Empty Optional Fields

Expected gaps, not bugs.

| Field | Missing | Total | % | Notes |
|-------|--------:|------:|--:|-------|
| `product.summary` | 180 | 564 | 31.9% | WooCommerce short description was blank — frontend hides this section when empty |
| `product.attributes` | 114 | 564 | 20.2% | Simple products with no variation options — expected |
| `product.dimensions.length/width/height` | ~41 | 564 | ~7.3% | Not all products had dimensions in WooCommerce |
| `product.descriptionImgs` | 26 | 564 | 4.6% | No images embedded in description HTML — expected |
| `product.description` | 17 | 564 | 3.0% | No description text — expected |
| `variation.description` | 2,459 | 5,364 | 45.8% | Most variations have no description — frontend falls back to parent |
| `variation.dimensions.length/width/height` | 179 | 5,364 | 3.3% | Variations without dimension data — expected |
| `variation.images` | 22 | 5,364 | 0.4% | Variations with no image — frontend falls back to parent product images |

---

## Notes

- `averageRating` and `reviewCount` are not present — dropped entirely. App builds its own review system.
- `product.attributes` empty (114 products) = simple products with no variants. Correct — they have no `variations[]` either.
- Variable products have `salePriceCents = null` — price range is `minPriceCents`–`maxPriceCents` derived from variations.
- Simple products have `minPriceCents = maxPriceCents = regularPrice`.
- Product attribute terms are trimmed to only what variations actually use — unused terms are silently removed during reshape.
