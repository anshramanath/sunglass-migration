# create-items audit — proSPORT Sunglasses

## Overview

- 166 items (150 variable, 16 simple)
- 3 flagged (see notes.md)
- 1713 variations embedded across 150 variable products

## Pricing

**Variable products (150):**
- `minPriceCents` range: 595–6795 cents ($5.95–$67.95)
- `maxPriceCents` range: 595–6795 cents ($5.95–$67.95)
- `sale=True`: 150/150 (100.0%)

**Simple products (16):**
- `minPriceCents` range: 595–3195 cents ($5.95–$31.95)
- `sale=True`: 16/16

## Variations per product

- min: 2  max: 88  avg: 11.4

## Image dedup

- 1677/1713 variations (97.9%) had `image` set to `null` — duplicate of a parent image
- 36 variations carry a unique image not present in the parent's `images[]`

## Product attributes (post-expansion + prune)

| Attribute | Products | Unique options |
|---|---|---|
| Color | 147 | 208 |
| Power | 65 | 13 |
| Activity | 6 | 2 |
| Frame Color | 6 | 1 |
| Frame Styles | 6 | 4 |
| Gender | 6 | 2 |
| Lens Color | 6 | 2 |
| Lens Type | 6 | 2 |
| Material | 6 | 1 |

## Variation attributes

| Attribute | Variations | Unique options |
|---|---|---|
| Color | 1663 | 208 |
| Power | 1399 | 13 |

## Stock

**Products:**
- `stock=0`: 11
- `stock=1`: 147
- `stock>1`: 8

**Variations:**
- `stock=0`: 299
- `stock=1`: 82
- `stock>1`: 1332

## Flagged

| Product | Reason |
|---|---|
| id=2211 proSPORT Professor Multifocal Reader | 1 unreplaced variation ID (2395 — SKU had space, excluded at validate) |
| id=2145 proSPORT Eliminator Polarized Bifocal | 16 unreplaced variation IDs + no filled variations (all had SKU spaces) |
| id=1208 proSPORT Morocco Mirror | 1 unreplaced variation ID (1355 — no price, excluded at validate) |
