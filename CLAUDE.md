# Sunglass Monster Migration — Claude Context
_Last updated: 2026-06-02_

## What this is
Multi-brand WooCommerce → Supabase migration pipeline. Uses the authenticated WooCommerce admin REST API (`/wp-json/wc/v3/`) for complete product data. The active brand is selected via `BRAND` in `.env`.

## Brand config

```python
BRAND_CONFIG = {
    "proSPORT Sunglasses": {
        "slug": "prosport",
        "base_url": "PROSPORT_BASE_URL",
        "consumer_key": "PROSPORT_CONSUMER_KEY",
        "consumer_secret": "PROSPORT_CONSUMER_SECRET",
    },
}
```

All pipeline scripts load `BRAND` from `.env`, look it up in `BRAND_CONFIG`, and derive the slug + credentials from there.

## Pipeline (in order)

### Products
1. `pipeline/fetch_products.py` — fetches all products via admin REST API → `data/{slug}/fetch-products/products.json`
2. `pipeline/slim_products.py` — extracts relevant fields only → `data/{slug}/slim-products/products.json`
3. `pipeline/validate_products.py` — validates all fields per product → `data/{slug}/validated-products/products.json` + `flagged.json`

### Variations
4. `pipeline/fetch_variations.py` — fetches all variations for each validated product → `data/{slug}/fetch-variations/variations.json`
5. `pipeline/slim_variations.py` — extracts relevant fields → `data/{slug}/slim-variations/variations.json`
6. `pipeline/validate_variations.py` — validates variations → `data/{slug}/validated-variations/variations.json` + `flagged.json`

### Reshape → Import
7. `pipeline/reshape_products.py` — normalizes products: HTML stripped, prices to cents, stock merged, attributes name-cleaned, descriptionImages as `{src, name}` objects → `data/{slug}/reshape-products/`
8. `pipeline/reshape_variations.py` — normalizes variations: same conventions, `image` → `images[]` array → `data/{slug}/reshape-variations/`
9. `pipeline/create_items.py` — embeds variations into products, ownership checks, attribute expansion/prune, image dedup, min/max price → `data/{slug}/create-items/`
10. `pipeline/prosport_categorize_items.py` — normalizes category names, assigns leaf paths with `{level, name, slug}` structure, hardcoded assignments for 21 uncategorized products → `data/{slug}/categorize-items/`
11. `pipeline/download_items.py` — downloads all images locally (crash-safe via `download_map.json`) → `data/{slug}/download-items/`
12. `pipeline/upload_items.py` — uploads to Supabase Storage (crash-safe via `upload_map.json`)
13. `pipeline/import_items.py` — inserts into Supabase DB

### Analysis (per stage)
- `analysis/analyze_products.py` — raw product field coverage and stats
- `analysis/analyze_slim_products.py` — slim product field presence and cross-checks
- `analysis/analyze_variations.py` — raw variation field coverage, pricing, stock, image, attribute stats
- `analysis/analyze_slim_variations.py` — slim variation field presence, on_sale consistency, parent_id cross-check

## Key differences from old pipeline

| | Old (BikerShades) | New (multi-brand) |
|---|---|---|
| API | Store API (unauthenticated) | Admin REST API (consumer key/secret) |
| Auth | None | HTTP Basic Auth |
| Stock | Binary `is_in_stock` bool | Real `stock_quantity` int |
| Prices | Inside `prices{}` object | Top-level strings |
| Variation images | `images[]` array (max 1) | `image` singular object |
| Brand selection | Hardcoded | `BRAND` env var + config dict |
| Output path | `migration/reshaped/` etc. | `data/{slug}/reshaped/` etc. |

## Admin API response shape (variation)

- `image` — singular object `{id, src, name, alt}` — the featured image
- `gallery_image_ids` — array of media IDs for additional images (empty on ProSport)
- `regular_price`, `sale_price` — top-level strings (not inside a `prices` object)
- `on_sale` — boolean, but verify with price comparison (same rule as before)
- `stock_quantity` — integer (real quantity), `manage_stock` bool
- `stock_status` — `"instock"` / `"outofstock"` / `"onbackorder"` string
- `attributes` — `[{id, name, slug, option}]` where `option` is the term name (not slug)

## Data paths

All output scoped to `data/{brand_slug}/`:
- `data/{slug}/fetch-products/products.json` — raw API response
- `data/{slug}/slim-products/products.json` — relevant fields only
- `data/{slug}/validate-products/products.json` + `flagged.json` — passed/failed validation (output folder: `validate-products/`)
- `data/{slug}/fetch-variations/variations.json` — raw variation API response
- `data/{slug}/slim-variations/variations.json` — relevant fields only
- `data/{slug}/validate-variations/variations.json` + `flagged.json` — passed/failed validation
- `data/{slug}/reshape-products/products.json` — normalized products
- `data/{slug}/reshape-variations/variations.json` — normalized variations
- `data/{slug}/create-items/items.json` + `flagged.json` — combined items
- `data/{slug}/categorize-items/items.json` — items with normalized `[[{level, name, slug}]]` category paths
- `data/{slug}/download-items/download_map.json` + `flagged.json` + `images/` — downloaded images

## Current state (ProSport)
- **Products:** 169 validated → reshaped → 166 items passed create-items, 3 flagged (products 2145, 2211, 1208 — unreplaced variation IDs from 18 variations excluded at validate: 17 SKU-spaces, 1 no-price).
- **Variations:** 1,740 validated → reshaped → 1,713 embedded into items.
- **Categorized:** 166 items → `categorize-items/`. 21 previously uncategorized products assigned. 9 leaves across 3 parent categories + Accessories root-level leaf.
- **Images:** 411 downloaded (373 product, 36 variation, 2 description) → `download-items/`. 0 failed.
- **Next step:** `upload_items.py`.
