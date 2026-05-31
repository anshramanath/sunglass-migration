# Downloaded Images Verify
_Last updated: 2026-05-30_

**Source:** `recategorized/categorized_items.json` cross-referenced against `url_map.json` and `failed.json`

---

## Result

**All critical checks passed.** Every image URL is accounted for — either downloaded or confirmed failed. No product is left imageless. 86 variations have no downloadable images; the frontend falls back to the parent product's images.

---

## Checks

| Check | Result |
|-------|--------|
| All image URLs accounted for (in map or failed) | ✅ 0 unaccounted |
| No URL in both `url_map` and `failed.json` | ✅ 0 duplicates |
| No extra URLs in `url_map` absent from items | ✅ 0 extra |
| No product has all product images failed | ✅ 0 affected |
| Variations with all images failed | ℹ️ 86 (frontend falls back to product) |

---

## Counts

| | Count |
|-|------:|
| URLs in items | 2,561 |
| In `url_map.json` | 2,531 |
| In `failed.json` | 30 |
| Unaccounted | 0 |
| Products with no images | 0 |
| Variations with no images | 86 |

---

## Notes

- The 86 variations with no images are pre-existing 404s from the WooCommerce server — the original images were deleted. The frontend falls back to parent product images naturally.
- Every product has at least one downloadable image, so no product page will appear broken.
