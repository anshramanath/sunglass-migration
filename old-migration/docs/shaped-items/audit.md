# Shaped Items Audit
_Last updated: 2026-05-31_

**Source:** `reshaped/shaped_items.json`
**Products:** 577 | **Variations:** 5,414

---

## Result

**Zero critical issues.** All required fields are present and valid across all 577 products and 5,414 variations.

---

## Critical Fields — All Pass

| Field | Status |
|-------|--------|
| `product.name/slug/sku/wpUrl/productUrl` | ✅ 577 / 577 |
| `product.minPriceCents` (> 0) | ✅ 577 / 577 |
| `product.maxPriceCents` (≥ minPriceCents) | ✅ 577 / 577 |
| `product.salePriceCents` (valid when sale=true, null for variable) | ✅ 577 / 577 |
| `product.stock` (0 or 1) | ✅ 577 / 577 |
| `variation.slug/sku/wpUrl/productUrl` | ✅ 5,414 / 5,414 |
| `variation.regularPriceCents` (> 0) | ✅ 5,414 / 5,414 |
| `variation.salePriceCents` (null ↔ sale=false, non-null and < regular ↔ sale=true) | ✅ 5,414 / 5,414 |
| `variation.stock` (0 or 1) | ✅ 5,414 / 5,414 |
| `variation.attribute` (not empty) | ✅ 5,414 / 5,414 |

---

## Informational — Empty Optional Fields

Expected gaps, not bugs.

| Field | Missing | Total | % | Notes |
|-------|--------:|------:|--:|-------|
| `product.summary` | 183 | 577 | 31.7% | WooCommerce short description was blank — frontend hides this section when empty |
| `product.attributes` | 121 | 577 | 21.0% | Simple products with no variation options — expected |
| `product.dimensions.length/width/height` | 49 | 577 | 8.5% | Dimensions are optional — partial or bad-unit dimensions silently nulled |
| `product.descriptionImgs` | 28 | 577 | 4.9% | No images embedded in description HTML — expected |
| `product.description` | 21 | 577 | 3.6% | No description text — expected |
| `product.weight` | 13 | 577 | 2.3% | Missing/0.0/bad-unit weight nulled — owner can fill in via dashboard |
| `variation.description` | 2,489 | 5,414 | 46.0% | Most variations have no description — frontend falls back to parent |
| `variation.images` | 3,513 | 5,414 | 64.9% | Variation images stripped if they duplicate a parent image — frontend falls back to product gallery |
| `variation.dimensions.length/width/height` | 175 | 5,414 | 3.2% | Variations without dimension data — expected |
| `variation.weight` | 12 | 5,414 | 0.2% | Missing/0.0/bad-unit weight nulled independently per variation |

---

## Notes

- `averageRating` and `reviewCount` are not present — dropped entirely. App builds its own review system.
- `product.attributes` empty (121 products) = simple products with no variation options. Correct — they have no `variations[]` either.
- Variable products have `salePriceCents = null` — price range is `minPriceCents`–`maxPriceCents` derived from variation regular prices (not effective prices). Frontend needs to query variations for actual sale prices.
- Simple products have `minPriceCents = maxPriceCents = regularPrice`. `salePriceCents` is null when not on sale, set when on sale.
- Variation `salePriceCents` is nullable: null when `sale=false`, a value (always < `regularPriceCents`) when `sale=true`. The `sale` bool is always the authoritative flag.
- `weight` and `weightUnit` treated like dimensions — if value is missing/0.0 OR unit is invalid/N/A, both are nulled. Each product and variation is checked independently. 14 products and 17 variations have null weight and are surfaced in the dashboard for the owner to fill in.
- `weightUnit` and `dimensionUnit` are derived from the last word of WooCommerce's `formatted_weight` / `formatted_dimensions` fields — not hardcoded.
- `product.dimensions` are optional. Partial dimensions or dimensions with a bad/missing unit are silently nulled (all three set to null, `dimensionUnit` set to null). 51 products (8.8%) have null dimensions.
- `variation.images` empty (65.0%) is expected — variation images that duplicate a parent product image are stripped during reshape. Frontend falls back to product gallery for those variations.
- Variations no longer have `descriptionImgs` — description images belong to products only. The 4 variation description images that existed were duplicates of the parent's description image.
- Product attribute terms are trimmed to only what variations actually use — unused terms stripped during reshape.
