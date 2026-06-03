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

- **166 products** imported (3 flagged: SKU spaces + missing price — fix in WooCommerce and re-run)
- **1,713 variations** imported
- **12 categories** (4 roots, 8 leaves), 197 product-category assignments
- **411 images** downloaded and uploaded to Supabase Storage bucket `prosport`
- Full summary: `new-migration/docs/build-run/migration-complete/summary.md`
