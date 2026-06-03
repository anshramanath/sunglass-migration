# slim-products analysis — Sunglass Monster

## Field presence

| Field | Present | Notes |
|---|---|---|
| id, name, slug, permalink, type, status, on_sale, featured, total_sales, stock_status, categories | 277/277 | OK |
| description | 256/277 | 21 missing |
| short_description | 147/277 | 130 missing |
| sku | 272/277 | 5 missing |
| price | 277/277 | OK |
| regular_price | 27/277 | Variable products have no parent regular_price — expected |
| sale_price | 25/277 | Same — variable products only |
| stock_quantity | 44/277 | Only when manage_stock=True |
| weight | 272/277 | 5 missing |
| dimensions | 248/277 | Kept (Monster has real data; ProSport had none) |
| images | 275/277 | 2 products have no images |
| attributes | 263/277 | 14 products have no attributes |
| variations | 250/277 | 27 simples have none — expected |

## Flags

- **5 no-SKU products:** 26307, 26166, 24707, 24573, 24554 — same as fetch analysis
- **0 draft products**
- **0 type/variations mismatches**

## on_sale vs sale_price

249 variable products have `on_sale=True` with no `sale_price` — WooCommerce quirk, same as ProSport. Real sale prices live on variations.

## stock_quantity vs stock_status

| has_qty | stock_status | Count |
|---|---|---|
| False | instock | 210 |
| False | outofstock | 23 |
| True | instock | 34 |
| True | outofstock | 10 |

23 products are `outofstock` with no quantity — these are primarily **proSPORT-branded products** sold on the Monster store. `stock_status` is the source of truth; `stock_quantity` used as supplementary data where available.

## Categories

64 unique categories. `"No category"` appears as a literal category name on 4 products. No "Uncategorized" tag (unlike ProSport). HTML entities (`&amp;`) present — strip at reshape.

## total_sales

118/277 products have `total_sales > 0`. 159 have 0 — treat as unknown.
