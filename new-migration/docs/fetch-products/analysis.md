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

One draft variable product exists — likely a copy/junk entry. Decide at reshape whether to drop it.

## Variations (parent-level IDs only)

- Total variation IDs across all variable products: **1,794**
- Per-product: min 2 / avg 11.6 / max 88

Actual variation data lives in `fetch_variations.py` output. The parent `variations` field is just an array of IDs.

## SKUs

- 170/171 products have a parent SKU (1 simple product missing)
- All 170 are unique at the parent level — no duplicates
- Variable product parent SKUs are meaningless; real SKUs live on variations

## Images (parent gallery)

All 171 products have at least one image. Most have multiple — these are the product gallery shots, not variation images.

| Image count | Products |
|---|---|
| 1 | 2 |
| 2 | 32 |
| 3 | 84 |
| 4 | 21 |
| 5 | 27 |
| 6+ | 5 |

Variation images come from the `image` field on each variation (fetched separately).

## Categories

11 unique categories. Every product is tagged **Uncategorized** alongside its real category — drop Uncategorized at reshape.

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
| BIFOCALS PROGRESSIVE | 2 |

## Attributes

9 unique attribute names across all products. Two types:

**Variation axes** (drive variation combinations):
- `Choose Color` — 154 products
- `Choose Power` — 68 products (bifocal/reader products only)

**Filter-only** (not variation axes, used for storefront filtering):
- `Frame Color for Filter` — 146
- `Lens Color for Filter` — 145
- `Activity for Filter` — 141
- `Frame Styles for Filter` — 139
- `Lens Type for Filter` — 135
- `Material for Filter` — 135
- `Gender For Filter` — 61

11 products have no attributes at all — inspect at reshape.

## Pricing (parent-level)

Parent `price` field is always populated (171/171) but is just a display value derived from variations. `regular_price` only exists on 17 products (the simple ones). `on_sale=True` on 170/171 — this is a WooCommerce quirk; actual sale logic lives on variations.

## Stock (parent-level)

- `manage_stock=True`: 19 products (actual quantity tracking)
- `stock_status`: 160 instock / 11 outofstock
- Variable product stock is aggregate of variations — per-variation stock comes from fetch_variations

## Descriptions

- Has `description`: 148 / 171
- Has `short_description`: 35 / 171

23 products have no description at all. Short description is sparse.

**Gotcha:** descriptions contain hardcoded Sunglass Monster image URLs (`sunglassmonster.com`). Decide at reshape whether to rewrite or strip them.

## Field coverage

~40 fields carry zero information (all null, all empty, or all-same WooCommerce defaults). See [notes.md](notes.md) for the full keep/drop lists.

Notable dead fields: `virtual`, `downloadable`, `tax_status`, `backorders_allowed`, `average_rating`, `rating_count`, `brands`, `tags`, `default_attributes`, `global_unique_id`, all `date_on_sale_*` fields.
