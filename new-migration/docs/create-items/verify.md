# create-items verify — proSPORT Sunglasses

## Result

`verify_create_items.py` — 166 items, 1713 variations — **PASSED**

## Checks

| Check | Rule |
|---|---|
| Coverage | Every source product is in exactly one of `items.json` or `flagged.json` |
| No overlap | No product appears in both files |
| No unreplaced IDs | `variations[]` contains only objects, no integers |
| Variation id in source list | Each embedded variation's `id` was in the original product's `variations[]` |
| `parent_id` matches | Each embedded variation's `parent_id` equals the product `id` |
| Variation in reshape-variations | Each embedded variation exists in `reshape-variations` under the correct `product_id` |
| Image dedup | No entry in a variation's `images[]` has a `src` matching any `src` in the parent's `images[]` |
| Variation attributes in parent pool | Each variation's `{name, option}` exists in the product's `attributes[]` after expansion |
| Simple products | `variations[]` is empty |
| `minPriceCents` | Equals `min(variation.regularPriceCents)` |
| `maxPriceCents` | Equals `max(variation.regularPriceCents)` |
| `sale` | Equals `any(variation.sale)` |
| Global variation ID uniqueness | No variation `id` appears across more than one product |
| Global SKU uniqueness | No SKU (product or variation) appears more than once across all items |
