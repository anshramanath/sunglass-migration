# Migration Complete — Run 1 (proSPORT Sunglasses)
_2026-06-02_

Full pipeline run. Schema applied fresh, Supabase Storage cleared before run.

## Pipeline results

| Stage | In | Out | Flagged |
|---|---|---|---|
| fetch_products | — | 171 | — |
| slim_products | 171 | 171 | — |
| validate_products | 171 | 169 | 2 (draft + no SKU) |
| fetch_variations | 169 products | 1,758 | — |
| slim_variations | 1,758 | 1,758 | — |
| validate_variations | 1,758 | 1,740 | 18 (17 SKU spaces, 1 no price) |
| reshape_products | 169 | 169 | — |
| reshape_variations | 1,740 | 1,740 | — |
| create_items | 169 + 1,740 | 166 items, 1,713 variations | 3 |
| prosport_categorize_items | 166 | 166, 197 leaf assignments | — |
| download_items | — | 411 images, 0 failed | — |
| upload_items | 411 | 411 → Supabase bucket `prosport` | — |
| import_items | 166 items | 166 products, 1,713 variations, 12 categories | — |

All verify scripts: **PASSED**

## DB state

| Table | Rows |
|---|---|
| brands | 1 |
| products | 166 |
| variations | 1,713 |
| categories | 12 (4 roots, 8 leaves) |
| product_categories | 197 |
| product_images | 565 |
| variation_images | 36 |
| description_images | 143 |

## Notes

- Two 503 errors during fetch_variations (id=1894, id=1657). Resolved on retry using crash-safe resume.
- 3 flagged products (2145, 2211, 1208) — fix SKU spaces + missing price in WooCommerce, then re-run pipeline to add them.
- `analyze_slim_products.py` had a stale `related_ids` reference — removed during this run.
