# Sunglass Monster Migration — Claude Context
_Last updated: 2026-06-01_

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

1. `pipeline/fetch_products.py` — fetches all products via admin REST API, saves to `data/{slug}/products.json`
2. `pipeline/fetch_variations.py` — fetches all variations per product, saves to `data/{slug}/variations.json`
3. `pipeline/reshape_items.py` — normalizes data, buckets by issue type into `data/{slug}/reshaped/`
4. `pipeline/recategorize_items.py` — applies drops/merges, collapses to leaf paths, outputs `data/{slug}/recategorized/`
5. `pipeline/download_images.py` — downloads all images locally (crash-safe via `url_map.json`)
6. `pipeline/upload_images.py` — uploads to Supabase Storage (crash-safe via `upload_map.json`)
7. `pipeline/import_items.py` — inserts categorized items into Supabase DB

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
- `data/{slug}/products.json`
- `data/{slug}/variations.json`
- `data/{slug}/reshaped/`
- `data/{slug}/recategorized/`
- `data/{slug}/images/` (url_map, upload_map, local/)

## Current state
- Folder structure created. Pipeline scripts not yet written.
- ProSport credentials confirmed working. 171 products (154 variable, 17 simple).
- No `gallery_image_ids` found on any ProSport variation — single `image` field only.
