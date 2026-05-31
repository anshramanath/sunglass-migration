# Shaped Items Audit
_Last updated: 2026-05-31_

**Source:** `reshaped/shaped_items.json`
**Products:** 586 | **Variations:** 5,771

---

## Result

**Zero critical issues.** All required fields are present and valid across all 586 products and 5,771 variations.

---

## Critical Fields — All Pass

| Field | Status |
|-------|--------|
| `product.name/slug/sku/wpUrl/productUrl` | ✅ 586 / 586 |
| `product.minPriceCents` (> 0) | ✅ 586 / 586 |
| `product.maxPriceCents` (≥ minPriceCents) | ✅ 586 / 586 |
| `product.salePriceCents` (valid when sale=true, null for variable) | ✅ 586 / 586 |
| `product.stock` (0 or 1) | ✅ 586 / 586 |
| `product.weight` (not null, > 0) | ✅ 586 / 586 |
| `variation.slug/sku/wpUrl/productUrl` | ✅ 5,771 / 5,771 |
| `variation.regularPriceCents` (> 0) | ✅ 5,771 / 5,771 |
| `variation.salePriceCents` (valid when sale=true) | ✅ 5,771 / 5,771 |
| `variation.stock` (0 or 1) | ✅ 5,771 / 5,771 |
| `variation.attribute` (not empty) | ✅ 5,771 / 5,771 |

---

## Informational — Empty Optional Fields

Expected gaps, not bugs.

| Field | Missing | Total | % | Notes |
|-------|--------:|------:|--:|-------|
| `product.summary` | 187 | 586 | 31.9% | WooCommerce short description was blank — frontend hides this section when empty |
| `product.attributes` | 114 | 586 | 19.5% | Simple products with no variation options — expected |
| `product.dimensions.length/width/height` | ~43 | 586 | ~7.3% | Not all products had dimensions in WooCommerce |
| `product.descriptionImgs` | 26 | 586 | 4.4% | No images embedded in description HTML — expected |
| `product.description` | 17 | 586 | 2.9% | No description text — expected |
| `variation.description` | 2,533 | 5,771 | 43.9% | Most variations have no description — frontend falls back to parent |
| `variation.dimensions.length/width/height` | 192 | 5,771 | 3.3% | Variations without dimension data — expected |
| `variation.images` | 22 | 5,771 | 0.4% | Variations with no image — frontend falls back to parent product images |

---

## Notes

- `averageRating` and `reviewCount` are not present — dropped entirely. App builds its own review system.
- `product.attributes` empty (114 products) = simple products with no variants. Correct — they have no `variations[]` either.
- Variable products have `salePriceCents = null` — price range is `minPriceCents`–`maxPriceCents` derived from variations.
- Simple products have `minPriceCents = maxPriceCents = regularPrice`.
