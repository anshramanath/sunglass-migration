# create-items analysis — run 1 (proSPORT Sunglasses)
_2026-06-02_

## Overview

166 items (150 variable, 16 simple), 1,713 variations, 3 flagged.

## Pricing

- Variable: minPriceCents median $25.95, max $67.95
- 141 products have flat pricing (min==max across all variations)
- 9 products have tiered pricing (Power readers — different prices per strength)
- Sale discount range: 15–47%, median 41%
- All 166 products sale=True, all 1,713 variations sale=True with salePriceCents set

## Stock

- Products: 11 out-of-stock, 147 stock=1 (fallback), 8 with real qty
- Variations: 299 out-of-stock (17.5%), 1,332 with real qty, total 9,497 units
- 2 variable products fully out of stock (Navigator Rimless, Eagle Eye HD Copper)
- 50 variable products partially out of stock

## Images

- 97.9% of variations have images=[] after dedup (1,677/1,713)
- 36 variations carry a unique image not in parent gallery
- Product images: min 1, max 13, avg 3.4 per product

## Attributes

- 9 product attribute names. Only Color (147 products) and Power (65) are meaningful variation axes — the rest (Activity, Frame Color, Frame Styles, Gender, Lens Color, Lens Type, Material) appear on only 6 products and have 1-2 options.
- 208 unique color options across all products
- Power options: 1.00–4.00 in 0.25 increments (13 values)

## Data quality signals

- 22 products with no description, summary, or description images
- 88 products with 0 total_sales (treat as unknown)
- No variation SKU/product SKU collisions
- Product stock vs sum(variation stock) differs on 147 products — expected, product.stock is the WC aggregate

## Categories (pre-categorize)

- 21 products with only Uncategorized (all handled by hardcoded assignments in prosport_categorize_items.py)
