# fetch-variations analysis — Sunglass Monster
_2,715 variations across 244 products_

## Overview

| | |
|---|---|
| Total variations | 2,715 |
| Products | 244 |
| Per-product: min / avg / max | 2 / 11.1 / 88 |
| All publish | 2,715 / 2,715 |

## SKUs

- 2,715 / 2,715 present
- 0 duplicates
- 0 missing

## Pricing

- Has price: 2,714 / 2,715 — 1 missing (same variation likely `purchasable=False`)
- Has regular_price: 2,714 / 2,715
- Has sale_price: 2,654 / 2,715
- `on_sale=True`: 2,654 — 61 variations not on sale (ProSport had all on sale)
- 0 cases of `on_sale=True` with no `sale_price`
- 1 variation `purchasable=False` — WooCommerce marks it unbuyable, almost certainly the no-price variation; will be flagged at validate_variations

## Stock

- `manage_stock=True`: 2,715 / 2,715 — all variations manage stock (unlike ProSport which was partial)
- `stock_quantity` always present as a result
- 2,057 instock / 658 outofstock (24.2%)
- Most common `stock_quantity`: 8 (1,095 variations) — likely a bulk-set default/placeholder

## Images

- All 2,715 variations have an image — unlike ProSport where most deduped to `[]`
- Image dedup at create_items will still run; variations whose image matches the parent gallery will be cleared

## Attributes

- 0 variations with no attributes
- 2 unique attribute names: `"Choose Color (REQUIRED)"` (2,714) and `"Choose Power"` (2,115)
- Both clean correctly via `clean_attr_name` → `Color`, `Power`

## Weight & Dimensions

- Weight: 2,715 / 2,715 (100%)
- Dimensions fully filled: 2,638 / 2,715 (97%)
- Both far richer than ProSport (which had no useful dimensions)

## Descriptions

- 603 / 2,715 variations have descriptions — primarily combo/bundle reader products
- ProSport had essentially none

## Dead fields

`virtual`, `downloadable`, `date_on_sale_*`, `backorders`, `backorders_allowed`, `backordered`, `global_unique_id` — all empty across all variations.
