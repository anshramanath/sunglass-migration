# fetch-products analysis — Sunglass Monster
_277 products fetched via admin REST API (`/wp-json/wc/v3/products`)_

## Type & status

| Type | Count |
|---|---|
| variable | 250 |
| simple | 27 |

| Status | Count |
|---|---|
| publish | 276 |
| private | 1 |

One private variable product: `Childrens Boys Girls Flip UP Shield` (id 26166). Flag at validate.

## Variations (parent-level IDs only)

- Total variation IDs across variable products: **2,796**
- Per-product: min 2 / avg 11.2 / max 88
- Simple products: 0 variation IDs

Actual variation data requires `fetch_variations.py`.

## SKUs

- 272/277 products have a parent SKU — 5 missing:
  - id 26307 `Socket Goggle` (simple)
  - id 26166 `Childrens Boys Girls Flip UP Shield` (variable)
  - id 24707 `Sunglass String Chum Strap` (simple)
  - id 24573 `VShield Vibrant...Bandannas` (variable)
  - id 24554 `Black Reusable Stretch Face Mask` (variable)
- 2 of the 5 no-SKU products are variable — more impactful than ProSport's single no-SKU simple
- All 272 present SKUs are unique

## Images

2 products have no images (ProSport had 0).

| Image count | Products |
|---|---|
| 0 | 2 |
| 1 | 4 |
| 2 | 77 |
| 3 | 116 |
| 4 | 23 |
| 5 | 47 |
| 6+ | 8 |

## Categories

64 unique categories — heavily gendered (Men's / Women's splits of same type). No "Uncategorized" tag present. 4 products tagged `"No category"` (literal category name, not missing data).

All 277 products have at least one category.

Top categories:
- Unisex Polarized: 87
- Men's Glasses: 80
- Men Sport, Golf & Cycling: 55
- Women Sport, Golf & Cycling: 54
- Women's Glasses: 53
- Men Polarized Bifocals & Readers: 51

HTML entities in category names (`&amp;`) — strip at reshape.

## Attributes

19 unique attribute names. 14 products have no attributes.

**Variation axes:**
- `Choose Color (REQUIRED)` — 246 products → will clean to `Color`
- `Choose Power` — 83 products → will clean to `Power`
- `Choose Color` — 1 product → already `Color`
- `Color` — 1 product → already clean
- `Choose Quantity` — 1 product (accessory)
- `Choose Bandana Color` — 1 product → will clean to `Bandana Color` (two words — warn)

**Filter-only:**
- `Frame Color for Filter` — 200
- `Lens Color for Filter` — 200
- `Activity for Filter` — 193
- `Frame Styles for Filter` — 193
- `Lens Type for Filter` — 189
- `Material for Filter` — 188
- `Gender For Filter` — 84
- `Special Size for Filter` — 7
- `Filter by Brand` — 7
- `Filter by Foam Type` — 2
- `Filter by Lens Type` — 2
- `Qty` — 2 (accessory products)
- `Cleaner Spray Bottle QTY` — 1 → multi-word after clean, will warn

## Pricing

`regular_price` and `sale_price` only populated on simple products (27). Variable products carry `price` only at the parent level — real prices live on variations. 249 products have `on_sale=True` with no `sale_price` — all variable, WooCommerce quirk (same as ProSport).

## Dimensions

248/277 products have populated dimensions — unlike ProSport (0/171). Worth keeping at slim.

## Stock

- `manage_stock=True`: 44 products
- `stock_status`: 244 instock / 33 outofstock

## Descriptions

- Has `description`: 256 / 277 (92%)
- Has `short_description`: 147 / 277 (53%) — richer than ProSport's 35/171

Descriptions contain hardcoded `sunglassmonster.com` image URLs — extract as descriptionImages at reshape.

## total_sales & featured

- `total_sales > 0`: 118 products (43%)
- `featured=True`: 2 products — Gemini (5965), Simi Sunglasses (5859)

## Field coverage

Dead fields (0% meaningful): `virtual`, `downloadable`, `date_on_sale_*`, `external_url`, `button_text`, `backorders_allowed`, `backordered`, `upsell_ids`, `cross_sell_ids`, `brands`, `tags` (1 product), `default_attributes`, `global_unique_id`, `post_password`.
