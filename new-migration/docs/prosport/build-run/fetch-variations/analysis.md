# fetch-variations analysis — proSPORT Sunglasses
_1758 variations across 153 variable products_

## Overview

| | |
|---|---|
| Variable products | 153 |
| Total variations | 1758 |
| Min per product | 2 |
| Max per product | 88 (proSPORT Jersey Sunglass Readers) |
| Avg per product | 11.5 |

Distribution (variation count → number of products):

`2:15  3:17  4:42  5:10  6:4  8:9  9:1  10:1  11:1  12:7  14:1  16:12  18:3  20:4  22:2  24:5  30:5  33:1  36:7  40:1  44:1  45:2  48:1  88:1`

## Status

All 1758 variations are `publish`. No drafts.

## SKUs

- All 1758 variations have a SKU
- All 1758 are unique
- No duplicates, no missing

## Pricing

| | Count |
|---|---|
| Has `price` | 1757 / 1758 |
| Has `regular_price` | 1757 / 1758 |
| Has `sale_price` | 1757 / 1758 |
| `on_sale=True` | 1757 / 1758 |
| `on_sale=True` with `sale_price` | 1757 |
| `on_sale=True` with no `sale_price` | 0 |

**`on_sale` is reliable on variations** — unlike parent products, every `on_sale=True` variation has an actual `sale_price`. Safe to use at reshape.

**1 variation with no price** — id=1355, parent=1208 (`proSPORT Morocco Mirror`), SKU=`CA25X095MRMIRROR`. Status is `publish`, `instock`, stock_quantity=8, but `price` is empty and `purchasable=False`. WooCommerce data issue — will be flagged at validation.

## Stock

`manage_stock=True` on all 1758. Every variation has a real `stock_quantity` — unlike parent products where most had none.

| Combination | Count |
|---|---|
| instock, qty > 0 | 1434 |
| outofstock, qty = 0 | 324 |

`stock_status` and `stock_quantity` are consistent on every variation. Either signal is reliable.

## Images

1758/1758 have an image with a valid `src`. No missing images.

Note: `image` is a singular object `{id, src, name, alt, ...}` — not an array.

## Attributes

Every variation has at least 1 attribute. These are the selected options per variation, not the parent's option list.

| Attribute | Variations |
|---|---|
| Choose Color | 1708 |
| Choose Power | 1439 |

- 1389 variations have both Color + Power (reader/bifocal products)
- 369 variations have Color only (non-reader sunglasses)

Only 2 unique attribute names across all 1758 variations.

## Weight / Dimensions

- **Weight**: 1757/1758 have a value. Values are `"2"` (1697), `"0.0"` (46), `"2.0"` (14). 1 missing.
- **Dimensions**: 0/1758 fully filled. Object always present but all subfields are empty strings — same as parent products. Drop at reshape.

## Description

429/1758 variations have a description. The rest are empty strings.

## Field coverage (notable)

| Field | Filled | Notes |
|---|---|---|
| `global_unique_id` | 0/1758 | Always `""` — drop at slim |
| `date_on_sale_from/to` | 0/1758 | Always null — drop at slim |
| `virtual` | 0/1758 | Always `False` — drop at slim |
| `downloadable` | 0/1758 | Always `False` — drop at slim |
| `tax_status` | 0/1758 | Always `"taxable"` — drop at slim |
| `backorders` | 0/1758 | Always `"no"` — drop at slim |
| `manage_stock` | 1758/1758 | Always `True` — drop at slim |
| `shipping_class` | 4/1758 | `1-2-sunglasses` on 4 variations — not relevant for import |
| `meta_data` | 154/1758 | Keys: `_woo_stock_sync_data` (cross-store sync artifact from BikerShades), `vcv-be-editor` (page builder). Neither useful — drop at slim |

## Flags

- **id=1355** (`proSPORT Morocco Mirror`, parent=1208, SKU=`CA25X095MRMIRROR`) — `publish`, instock, qty=8, but no price and `purchasable=False`. Will be flagged at validation.
