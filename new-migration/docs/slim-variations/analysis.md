# slim-variations analysis — proSPORT Sunglasses
_1758 variations across 153 products after slimming from fetch-variations_

## Field presence

"Filled" means a genuinely valid value. `dimensions` requires all three subfields non-empty. `image` requires a non-empty `src`. `attributes` requires at least one entry.

| Field | Filled | Notes |
|---|---|---|
| `id` | 1758/1758 | |
| `parent_id` | 1758/1758 | |
| `name` | 1758/1758 | |
| `type` | 1758/1758 | Always `"variation"` |
| `status` | 1758/1758 | All `publish` — no drafts |
| `description` | 429/1758 | Sparse — 1329 variations have no description |
| `permalink` | 1758/1758 | |
| `sku` | 1758/1758 | All unique |
| `price` | 1757/1758 | 1 missing — id=1355 |
| `regular_price` | 1757/1758 | 1 missing — id=1355 |
| `sale_price` | 1757/1758 | 1 missing — id=1355 |
| `on_sale` | 1758/1758 | Reliable — see below |
| `stock_quantity` | 1758/1758 | All have a real quantity |
| `stock_status` | 1758/1758 | |
| `weight` | 1757/1758 | 1 missing |
| `dimensions` | 0/1758 | Object always present but all subfields empty. Drop at reshape. |
| `image` | 1758/1758 | |
| `attributes` | 1758/1758 | 1–2 attributes per variation |

## Flags

- **id=1355** (parent=1208 `proSPORT Morocco Mirror`, SKU=`CA25X095MRMIRROR`) — no `price`, `regular_price`, or `sale_price`. `instock` with `stock_quantity` set. Will be flagged at validation.

## on_sale truthfulness

`on_sale` is fully reliable on variations — unlike parent products:

- `on_sale=True` with no `sale_price`: **0**
- `sale_price` present but `on_sale=False`: **0**

Every `on_sale=True` variation has a real `sale_price`. Safe to use directly at reshape.

## Stock

All 1758 variations have `manage_stock=True` and a real `stock_quantity`. `stock_status` and `stock_quantity` are consistent on every variation.

| Combination | Count |
|---|---|
| instock, has quantity | 1434 |
| outofstock, has quantity (qty=0) | 324 |

## Attributes

| Attribute count | Variations |
|---|---|
| 1 (Color only) | 369 |
| 2 (Color + Power) | 1389 |

Only 2 unique attribute names across all 1758 variations: `Choose Color` (1708) and `Choose Power` (1439).

## Weight

- Has weight: 1757/1758
- Values: `"2"` (1697), `"0.0"` (46), `"2.0"` (14)

## parent_id cross-check

0 mismatches — every variation's `parent_id` matches the `product_id` key it was fetched under.
