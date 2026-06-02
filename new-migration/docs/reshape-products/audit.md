# reshape-products audit — proSPORT Sunglasses

## Overview

- 169 products (153 variable, 16 simple)
- All 169 have images; no products have real dimension values (all fields null)

## Field presence

| Field | Present |
|---|---|
| `description` | 147/169 (87.0%) |
| `descriptionImages` | 146/169 (86.4%) |
| `shortDescription` | 32/169 (18.9%) |
| `weight` | 18/169 (10.7%) |
| `dimensions` (any non-null field) | 0/169 (0.0%) |
| `images` | 169/169 (100.0%) |

## Pricing

**Simple products (16):**
- All 16 are on sale (`sale=True`)
- `minPriceCents` range: 595–3195 cents ($5.95–$31.95)
- `salePriceCents` range: 395–1795 cents

**Variable products (153):**
- `minPriceCents`, `maxPriceCents`, `salePriceCents` all null (deferred to combine step)
- `sale=True` on all 153 — WooCommerce value; verified accurate against validated variations (see notes.md)

## Stock

- `stock=0`: 11 products (outofstock or zero quantity)
- `stock=1`: 149 products (instock fallback — no real quantity tracked)
- `stock>1`: 9 products (real stock_quantity from WooCommerce)

## Weight

- 18/169 products have a weight value; range 0.0–2.0

## Images

- 576 total image objects across 169 products
- Per product: min 1, max 13, avg 3.4

## Description images

- 146 products have 1 description image; 23 have none
- Only 2 unique URLs across all products (reused sizing diagrams from sunglassmonster.com and bikershades.com)

## Short description

- 32 products have a shortDescription
- 4–7 bullet points per product (avg 5.6)

## Categories

11 unique categories. All 169 products have at least one.

| Category | Products |
|---|---|
| Uncategorized | 169 |
| READERS SPECIAL FIT | 67 |
| BIFOCALS | 45 |
| POLARIZED | 36 |
| SPORT | 31 |
| FULL LENS | 24 |
| HD COPPER | 15 |
| CLEAR & YELLOW | 11 |
| STREET | 10 |
| METALS & AVIATORS | 6 |

Note: all 169 products are also assigned to "Uncategorized" — this category will be dropped at recategorize.

## Attributes

| Attribute | Products | Unique options |
|---|---|---|
| Color | 153 | 214 |
| Frame Color | 146 | 27 |
| Lens Color | 145 | 20 |
| Activity | 141 | 8 |
| Frame Styles | 139 | 9 |
| Lens Type | 135 | 7 |
| Material | 135 | 3 |
| Power | 67 | 21 |
| Gender | 61 | 2 |
