# import-items notes — proSPORT Sunglasses

## Results

- Input: `categorize-items/items.json` (166 items, 1713 variations)
- Script: `pipeline/import_items.py`
- DB: Supabase/Postgres — `001_initial_schema.sql`

## What this step does

Inserts all products, variations, categories, and images into the Supabase database. Resolves image URLs through the two-map chain before writing to image tables. Each run wipes existing data (`TRUNCATE brands CASCADE`) before inserting.

## Image resolution chain

```
original URL → download_map → local path → upload_map → Supabase storage URL
```

If either lookup fails the image is silently dropped. Product images that fail to resolve were already caught at `verify_download_items.py` — no product is left imageless.

## Category insertion

Categories are inserted lazily via `ensure_category(path)`. Each path in `[[{level, name, slug}]]` is walked root-to-leaf — missing nodes are inserted, existing nodes reuse their cached UUID. Each product is linked to its leaf category IDs via `product_categories`.

## Field mapping

| JSON field | DB column | Notes |
|---|---|---|
| `name` | `products.name` | |
| `slug` | `products.slug` | |
| `sku` | `products.sku` | unique |
| `oldUrl` | `products.old_url` | |
| `description` | `products.description` | nullable |
| `summary` | `products.summary` | text[] |
| `attributes` | `products.attributes` | jsonb |
| `featured` | `products.featured` | |
| `totalSales` | `products.total_sales` | |
| `sale` | `products.sale` | |
| `minPriceCents` | `products.min_price_cents` | |
| `maxPriceCents` | `products.max_price_cents` | |
| `salePriceCents` | `products.sale_price_cents` | nullable |
| `stock` | `products.stock` | |
| `weight` | `products.weight` | nullable |
| `dimensions.length/width/height` | `products.length/width/height` | all null for ProSport |
| `variations[].sku` | `variations.sku` | unique |
| `variations[].attributes` | `variations.attributes` | jsonb `[{name, option}]` |
| `variations[].regularPriceCents` | `variations.regular_price_cents` | |
| `variations[].salePriceCents` | `variations.sale_price_cents` | nullable |

WooCommerce `id` and `parent_id` are used only for linking during import and are not stored. The DB generates fresh UUIDs for all rows.
