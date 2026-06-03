# create-items — Notes

## Run summary
- Input: 267 reshape-products + 2,673 reshape-variations
- Output: **265 items** (240 variable, 25 simple), **2 flagged**
- Variations embedded: **2,646**

## Flagged products (2)

Both flagged due to unreplaced variation IDs — one variation per product failed validation upstream and was excluded, leaving a dangling ID in the parent's variation list.

| id | name | missing variation | root cause |
|----|------|-------------------|------------|
| 10471 | proSPORT Professor Multifocal Reader | 11143 | SKU space in variation |
| 6688 | proSPORT Morocco Mirror | 7682 | no price on variation |

Fix in WooCommerce: correct the variation data, re-fetch from that product down, re-run pipeline.

## Notable data points
- 100% of products have `sale=True` — all are on sale relative to their regular price.
- 96.3% of variation images are deduped (match the first variation for that product) → `images=[]`.
- 97 variations have their own unique image.
- 19 products have no description, summary, or descriptionImages at all.
- 221 variable products have flat pricing (all variations same regularPriceCents).
- 1 variation (id under product 8826) has only `Power` attribute vs parent's `[Color, Power]` — a WooCommerce data gap, not a pipeline issue.
