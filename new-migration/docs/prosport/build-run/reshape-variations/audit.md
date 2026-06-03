# reshape-variations audit — proSPORT Sunglasses

## Overview

- 1740 variations across 152 products
- 2–88 variations per product (avg 11.4)

## Field presence

| Field | Present |
|---|---|
| `description` | 413/1740 (23.7%) |
| `weight` | 1740/1740 (100.0%) |
| `dimensions` (any non-null field) | 0/1740 (0.0%) |

## Images

- All 1740 variations have a non-empty `images[]` — source `image` field is always populated at this stage
- 209 unique image URLs
- Dedup against parent images happens at create-items, not here

## Pricing

- All 1740 variations have `sale=True` — every ProSport variation is on sale
- `regularPriceCents` range: 595–6795 cents ($5.95–$67.95)
- `salePriceCents` range: 495–5099 cents ($4.95–$50.99)
- `regularPriceCents=null`: 0
- `salePriceCents=null`: 0

## Stock

- `stock=0` (outofstock / zero quantity): 317
- `stock=1` (instock fallback — no manage_stock): 82
- `stock>1` (real quantity): 1341

## Weight

- All 1740 variations have a weight value
- Range: 0.0–2.0

## Attributes

| Attribute | Variations | Unique options |
|---|---|---|
| Color | 1690 | 208 |
| Power | 1422 | 17 |

Note: 1690 variations have Color (not all have Power — non-bifocal products only use Color).

## Variations per product

| Variations | Products |
|---|---|
| 2 | 15 |
| 3 | 17 |
| 4 | 43 |
| 5 | 9 |
| 6 | 4 |
| 8 | 9 |
| 9–11 | 3 |
| 12 | 7 |
| 14–16 | 12 |
| 18–24 | 14 |
| 30–48 | 14 |
| 88 | 1 |
