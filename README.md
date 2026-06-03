# Sunglass Monster Migration
Migrates brand product data from WooCommerce to Supabase using the authenticated admin REST API.

---

## Brands

| Brand | Slug | Store URL | Status |
|-------|------|-----------|--------|
| proSPORT Sunglasses | `prosport` | prosportsunglasses.com | ✅ Complete |
| Sunglass Monster | `monster` | sunglassmonster.com | 🔄 In Progress |

Set `BRAND=prosport` or `BRAND=monster` in `.env` to select the active brand.

---

## Structure

```
new-migration/
  pipeline/      ← fetch, slim, validate, reshape, create, categorize, download, upload, import
  analysis/      ← per-stage field coverage and stats scripts
  qa/            ← per-stage audit and verify scripts
  config/        ← shared BRAND_CONFIG + load_brand() module
  db/            ← schema SQL (001_initial_schema.sql, drop_schema.sql)
  data/          ← per-brand output (data/{slug}/...)
  docs/
    prosport/
      build-run/ ← notes from building the pipeline
      run-1/     ← full ProSport migration run notes + summary
    monster/
      build-run/ ← Monster migration run notes (in progress)
```

---

## Running

```bash
# Set active brand in .env
BRAND=monster  # or prosport

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

# Categorize → import (categorize script is brand-specific)
python pipeline/monster_categorize_items.py   # or prosport_categorize_items.py
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

BRAND=monster

PROSPORT_BASE_URL=https://prosportsunglasses.com
PROSPORT_CONSUMER_KEY=...
PROSPORT_CONSUMER_SECRET=...

MONSTER_BASE_URL=https://sunglassmonster.com
MONSTER_CONSUMER_KEY=...
MONSTER_CONSUMER_SECRET=...
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

Full summary: `new-migration/docs/prosport/run-1/migration-complete/summary.md`

---

## Monster — In Progress

| Stage | Count | Status |
|-------|-------|--------|
| fetch-products | 277 | ✅ |
| validate-products | 267 passed, 10 flagged | ✅ |
| fetch-variations | 242 products, 2,673 variations | ✅ |
| validate-variations | 2,673 passed, 2 flagged | ✅ |
| reshape-products | 267 | ✅ |
| reshape-variations | 2,673 | ✅ |
| create-items | 265 items, 2 flagged | ✅ |
| categorize-items | — | ⏳ Next |
| download-items | — | ⏳ |
| upload-items | — | ⏳ |
| import | — | ⏳ |

12 items to fix in WooCommerce before they can be imported (10 flagged products + 2 flagged create-items).
