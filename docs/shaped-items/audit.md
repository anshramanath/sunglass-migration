# Clean Products Audit Report
_Last updated: 2026-05-30_

**Source:** `reshaped/clean_products_shape.json`
**Products:** 586 | **Variations:** 5,771

---

## Result

**Zero critical issues.** All required fields are present and valid across all 586 products and 5,771 variations.

---

## Critical Fields — All Pass

| Field | Status |
|-------|--------|
| `product.name/slug/sku/wpUrl/productUrl` | ✅ 586 / 586 |
| `product.regularPriceInCents` (> 0) | ✅ 586 / 586 |
| `product.salePriceInCents` (valid when sale=true) | ✅ 586 / 586 |
| `product.averageRating` (0–5) | ✅ 586 / 586 |
| `product.weight` (not null, > 0) | ✅ 586 / 586 |
| `variation.slug/sku/wpUrl/productUrl` | ✅ 5,771 / 5,771 |
| `variation.regularPriceInCents` (> 0) | ✅ 5,771 / 5,771 |
| `variation.salePriceInCents` (valid when sale=true) | ✅ 5,771 / 5,771 |
| `variation.attribute` (not empty) | ✅ 5,771 / 5,771 |

---

## Informational — Empty Optional Fields

These are expected gaps, not bugs. Noted here for visibility.

| Field | Missing | Total | % | Notes |
|-------|--------:|------:|--:|-------|
| `product.summary` | 187 | 586 | 31.9% | WooCommerce short description was blank — frontend should hide this section when empty |
| `product.attributes` | 114 | 586 | 19.5% | Simple products with no variation options — expected |
| `product.dimensions.length/width/height` | ~43 | 586 | ~7.3% | Not all products had dimensions in WooCommerce |
| `product.descriptionImgs` | 26 | 586 | 4.4% | Products with no images embedded in description HTML — expected |
| `product.description` | 17 | 586 | 2.9% | Products with no description text — expected |
| `variation.description` | 2,533 | 5,771 | 43.9% | Most variations have no description — frontend falls back to parent product description |
| `variation.dimensions.length/width/height` | 192 | 5,771 | 3.3% | Variations without dimension data — expected |
| `variation.images` | 22 | 5,771 | 0.4% | Variations with no image — frontend falls back to parent product images |

---

## Notes

- `product.categories` is now a flat array of WooCommerce link URLs. The audit does not flag empty categories — all 586 products have at least one category link.
- `product.attributes` being empty (114 products) means those are simple products with no color/power/size variants. This is correct — they have no `variations[]` either.
- The 22 variations with no images are pre-existing gaps in the WooCommerce data (images 404'd during a previous download attempt). Frontend handles this gracefully by falling back to parent product images.
