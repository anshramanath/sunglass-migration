# fetch-products analysis — proSPORT Sunglasses
_171 products fetched via admin REST API (`/wp-json/wc/v3/products`)_

## Type & status

| Type | Count |
|---|---|
| variable | 154 |
| simple | 17 |

| Status | Count |
|---|---|
| publish | 170 |
| draft | 1 |

One draft variable product: `proSPORT Cabriolet Mirror Bifocal (Copy)` (id 4019). Likely a junk copy — flag at reshape.

## Variations (parent-level IDs only)

- Total variation IDs across variable products: **1,794**
- Per-product: min 2 / avg 11.6 / max 88
- Simple products: 0 variation IDs

Actual variation data requires `fetch_variations.py`. The parent `variations` field is just an array of IDs.

## SKUs

- 170/171 products have a parent SKU — missing on `Sunglass String Chum Strap` (id 3139, simple)
- All 170 are unique at the parent level
- Variable product parent SKUs are meaningless; real SKUs live on variations — nullify at reshape

## Images (parent gallery)

All 171 products have at least one image. Most have multiple — parent gallery shots, not variation images.

| Image count | Products |
|---|---|
| 1 | 2 |
| 2 | 32 |
| 3 | 84 |
| 4 | 21 |
| 5 | 27 |
| 6+ | 5 |

## Categories

11 unique categories. Every product is tagged **Uncategorized** alongside its real category — strip at reshape.

| Category | Products |
|---|---|
| Uncategorized | 171 |
| READERS SPECIAL FIT | 68 |
| BIFOCALS | 46 |
| POLARIZED | 36 |
| SPORT | 31 |
| FULL LENS | 24 |
| HD COPPER | 15 |
| CLEAR & YELLOW | 11 |
| STREET | 10 |
| METALS & AVIATORS | 6 |
| BIG & TALL | 2 |

## Attributes

9 unique attribute names. Two types:

**Variation axes** (drive variation combinations):
- `Choose Color` — 154 products
- `Choose Power` — 68 products (bifocal/reader products only)

**Filter-only** (storefront filtering, not variation axes):
- `Frame Color for Filter` — 146
- `Lens Color for Filter` — 145
- `Activity for Filter` — 141
- `Frame Styles for Filter` — 139
- `Lens Type for Filter` — 135
- `Material for Filter` — 135
- `Gender For Filter` — 61

11 products have no attributes — inspect at reshape.

## Pricing

Parent `price` is always populated but derived from variations for variable products. `regular_price` and `sale_price` only exist on simple products.

`on_sale=True` on 170/171 products — WooCommerce sets this when any variation is on sale. 154 products have `on_sale=True` with no `sale_price` at the parent level, all of them variable. Reliable for simple products only.

## Dimensions

All 171 products have a `dimensions` object but every subfield (`length`, `width`, `height`) is an empty string — 0/171 usable. Drop at reshape.

## total_sales & featured

- `total_sales > 0`: 80 products. Top values: 1×22, 3×12, 4×11, 2×11. Treat 0 as unknown, not confirmed zero.
- `featured=True`: 5 products — Apex Day Vision, Puma Bifocal, Methane Bifocal, Taxi Polarized Bifocal, Commando Polarized Bifocal.

## Stock

- `manage_stock=True`: 19 products
- `stock_status`: 160 instock / 11 outofstock
- `stock_quantity` only valid when `manage_stock=True`. Use `stock_status` as source of truth.

## Descriptions

- Has `description`: 148 / 171
- Has `short_description`: 35 / 171

Descriptions contain hardcoded Sunglass Monster image URLs (`sunglassmonster.com`). Decide at reshape whether to rewrite or strip.

## Field coverage summary

~40 fields carry zero information. Notable dead fields: `virtual`, `downloadable`, `tax_status`, `backorders_allowed`, `average_rating`, `rating_count`, `brands`, `tags`, `default_attributes`, `global_unique_id`, all `date_on_sale_*` fields, `dimensions` (object exists but all empty). See [notes.md](notes.md) for full keep/drop lists.
