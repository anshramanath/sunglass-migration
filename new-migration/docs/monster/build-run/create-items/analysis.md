# create-items — Analysis

## Counts
- Items: 265 (variable: 240, simple: 25)
- Variations: 2,646
- Flagged: 2

## Pricing
- All 265 products have `sale=True`
- Variable products: min=$5.95, max=$67.95
- Simple products: min=$5.95, max=$31.95
- 221 variable products have flat pricing (all variations same regularPrice)
- 19 tiered-price products (min < max); widest spread = $15 (Jersey Sun Reader)
- Variations: 2,586/2,646 (97.7%) have salePriceCents set
- Discount depth: median 38%, max 51%

## Attributes
- 11 unique product attribute names post-expansion; 2 variation attribute names
- Color: dominant — 240 products, 329 unique options
- Power: 79 reader/bifocal products, 14 options (+0.50 → +4.00)
- Brand/Activity/Style/Gender/etc: 6 Locs products each
- 1 variation under product 8826 has only `Power` (missing `Color`) — WooCommerce data gap

## Images
- 590 unique product image URLs
- 96.3% of variations have `images=[]` (deduped)
- 97 variations have their own image (3.7%)
- 230 variable products: all variation images are null

## Stock
- Variable product stock: null (240 products)
- Simple product stock: 10 out-of-stock, 15 in-stock with real quantity
- Variation stock: 637 out-of-stock (24.1%), 1,863 with real quantity
- 25 variable products fully out of stock (all variations stock=0)
- 92 variable products partially out of stock

## Description coverage
- description present: 246/265 (92.8%)
- descriptionImages non-empty: 241/265 (90.9%)
- summary non-empty: 136/265 (51.3%)
- 17 products have none of the above — no content at all

## SKU
- All 265 products + 2,646 variations have SKUs
- No duplicates, no collisions between product and variation SKUs

## Categories (pre-categorize step)
- 61 unique WooCommerce category names attached to items
- 4 products in "No category"
- Products per product: min=1, max=18, avg=3.4
