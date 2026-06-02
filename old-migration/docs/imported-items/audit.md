# Imported Items Audit
_Last updated: 2026-06-01_

**Source:** Supabase DB
**Products:** 573 | **Variations:** 5,296 | **Categories:** 56

---

## Result

**All checks passed.** Row counts match source exactly. No products without images or categories. No duplicate SKUs.

---

## Row Counts

| Table | DB | Expected |
|-------|---:|--------:|
| `products` | 573 | 573 ✅ |
| `variations` | 5,296 | 5,296 ✅ |
| `categories` | 56 | — |
| `product_categories` | 1,067 | — |
| `product_images` | 2,530 | — |
| `variation_images` | 1,899 | — |
| `description_images` | 912 | — |

---

## Category Tree

| Depth | Count |
|-------|------:|
| 1 | 8 |
| 2 | 20 |
| 3 | 28 |

---

## Data Quality

| Check | Result |
|-------|--------|
| Products with no images | 0 ✅ |
| Products with no categories | 0 ✅ |
| Variations with no image | 3,409 (frontend falls back to product) |
| Duplicate product SKUs | 0 ✅ |
| Duplicate variation SKUs | 0 ✅ |

---

## Brands

- BikerShades (`slug=bikershades`)

---

## Notes

- `variation_images` replaces the previous `image_src`/`image_name` columns on variations — supports multiple images per variation with `sort_order`.
- 10 variation images dropped at import (permanent 404s — in `failed.json`, not in `url_map`). All affected variations still have parent product images for frontend fallback.
- `description_images` is product-only — variation description images were removed during reshape (always duplicates of parent).
