# Sunglass Monster Migration
Migrates brand product data from WooCommerce to Supabase using the authenticated admin REST API.

---

## Brands

| Brand | Slug | Store URL | Status |
|-------|------|-----------|--------|
| proSPORT Sunglasses | `prosport` | prosportsunglasses.com | ✅ Complete |

Set `BRAND=prosport` in `.env` to select the active brand.

---

## Structure

```
new-migration/
  pipeline/      ← fetch, slim, validate, reshape, create, categorize, download, upload, import
  analysis/      ← per-stage field coverage and stats scripts
  qa/            ← per-stage audit and verify scripts
  db/            ← schema SQL (001_initial_schema.sql, drop_schema.sql)
  data/          ← per-brand output (data/{slug}/...)
  docs/
    build-run/   ← notes from building the pipeline (one-time)
    run-1/       ← notes from the first full ProSport run
```

---

## Running

```bash
# Set active brand in .env
BRAND=prosport

# Products
python pipeline/fetch_products.py
python pipeline/slim_products.py
python pipeline/validate_products.py

# Variations
python pipeline/fetch_variations.py
python pipeline/slim_variations.py
python pipeline/validate_variations.py

# Reshape → create items
python pipeline/reshape_products.py
python pipeline/reshape_variations.py
python pipeline/create_items.py

# Categorize → import
python pipeline/prosport_categorize_items.py
python pipeline/download_items.py
python pipeline/upload_items.py
python pipeline/import_items.py
```

---

## Environment

`.env` at repo root. Required variables:

```env
DATABASE_URL=...
SUPABASE_URL=...
SUPABASE_SERVICE_KEY=...

BRAND=prosport

PROSPORT_BASE_URL=https://prosportsunglasses.com
PROSPORT_CONSUMER_KEY=...
PROSPORT_CONSUMER_SECRET=...
```

---

## ProSport — Run 1

| Table | Rows |
|-------|------|
| products | 166 |
| variations | 1,713 |
| categories | 12 (4 roots, 8 leaves) |
| product_categories | 197 |
| product_images | 565 |
| variation_images | 36 |
| description_images | 143 |

All verify scripts: **PASSED**

3 products flagged (2145, 2211, 1208) — fix SKU spaces + missing price in WooCommerce, re-run pipeline to add them.

Full summary: `new-migration/docs/run-1/migration-complete/summary.md`
