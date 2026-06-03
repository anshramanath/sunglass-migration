# slim-variations analysis — Sunglass Monster

## Field presence

| Field | Present | Notes |
|---|---|---|
| id, parent_id, name, type, status, permalink, sku, on_sale, stock_quantity, stock_status, weight, image, attributes | 2715/2715 | OK |
| description | 603/2715 | 2112 missing — combo/bundle readers only |
| price | 2714/2715 | 1 missing |
| regular_price | 2714/2715 | 1 missing (same variation) |
| sale_price | 2654/2715 | 61 not on sale |
| dimensions | 2638/2715 | 77 missing |

## Flags

- **1 no-price variation:** id=7682, SKU `CA25X095MRMIRROR-0`, parent=6688 — will be flagged at validate_variations
- **0 no-SKU variations**
- **0 non-publish variations**

## on_sale consistency

- 0 cases of `on_sale=True` with no `sale_price`
- 0 cases of `sale_price` set but `on_sale=False`
- Fully consistent — cleaner than ProSport

## Stock

All 2,715 variations have `stock_quantity` (manage_stock=True on all). 2,057 instock, 658 outofstock. No ambiguous cases.

## Attributes

2 unique names: `"Choose Color (REQUIRED)"` (2,714) and `"Choose Power"` (2,115). Both clean to single words at reshape. 0 parent_id mismatches.
