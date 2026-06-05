# Sunglass Monster Migration
Migrates brand product data from WooCommerce to Supabase using the authenticated admin REST API.

---

## Brands

| Brand | Slug | Store URL | Status |
|-------|------|-----------|--------|
| proSPORT Sunglasses | `prosport` | prosportsunglasses.com | 🔄 create-items done, categorize → download → upload → import next |
| Sunglass Monster | `monster` | sunglassmonster.com | 🔄 create-items done, write monster_categorize_items.py next |
| BikerShades | `bikershades` | bikershades.com | 🔄 create-items done, write bikershades_categorize_items.py next |

Set `BRAND=prosport`, `BRAND=monster`, or `BRAND=bikershades` in `.env` to select the active brand.

---

## Structure

```
new-migration/
  pipeline/      ← fetch, slim, validate, reshape, create, categorize, download, upload, import
  analysis/      ← per-stage field coverage and stats scripts
  qa/            ← per-stage audit, verify, and informational check scripts
  config/        ← shared BRAND_CONFIG + load_brand() module
  db/            ← schema SQL (001_initial_schema.sql, drop_schema.sql)
  data/          ← per-brand output (data/{slug}/...)
  product-funnel.md ← per-stage counts, flagging rationale, open questions
  docs/
    prosport/
      build-run/ ← notes from building the pipeline
      run-1/     ← full ProSport run-1 notes + summary (old pipeline)
      run-2/     ← ProSport run-2 (all pipeline improvements applied)
    monster/
      build-run/ ← Monster migration run notes
    bikershades/
      build-run/ ← BikerShades migration run notes
```

---

## Running

```bash
# Set active brand in .env
BRAND=bikershades  # or prosport, monster

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
python pipeline/bikershades_categorize_items.py   # or prosport_ / monster_
python pipeline/download_items.py
python pipeline/upload_items.py
python pipeline/import_items.py

# QA / analysis (run at each stage)
python qa/veeqo_items.py        # informational Veeqo SKU check (stdout only)
python analysis/analyze_items.py
python qa/audit_create_items.py
python qa/verify_create_items.py
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

BIKERSHADES_BASE_URL=https://bikershades.com
BIKERSHADES_CONSUMER_KEY=...
BIKERSHADES_CONSUMER_SECRET=...
```

---

## ProSport — Run 1 (complete, old pipeline)

| Table | Rows |
|-------|------|
| products | 166 |
| variations | 1,713 |
| categories | 12 (4 roots, 8 leaves) |
| product_categories | 197 |
| product_images | 565 |
| variation_images | 36 |
| description_images | 143 |

All verify scripts: **PASSED**. Full summary: `new-migration/docs/prosport/run-1/migration-complete/summary.md`

---

## Current pipeline state (full re-run from scratch)

### ProSport

| Stage | Count | Status |
|-------|-------|--------|
| validate-products | 169 passed, 2 flagged | ✅ |
| validate-variations | 1,669 passed, 89 flagged | ✅ |
| create-items | 161 items, 8 flagged, 1,646 vars | ✅ |
| categorize-items | — | ⏳ Next |
| download-items | — | ⏳ |
| upload-items | — | ⏳ |
| import | — | ⏳ |

### Monster

| Stage | Count | Status |
|-------|-------|--------|
| validate-products | 267 passed, 10 flagged | ✅ |
| validate-variations | 2,560 passed, 115 flagged | ✅ |
| create-items | 260 items, 7 flagged, 2,537 vars | ✅ |
| categorize-items | — | ⏳ Write script next |
| download-items | — | ⏳ |
| upload-items | — | ⏳ |
| import | — | ⏳ |

### BikerShades

| Stage | Count | Status |
|-------|-------|--------|
| validate-products | 611 passed, 93 flagged | ✅ |
| validate-variations | 5,299 passed, 694 flagged | ✅ |
| create-items | 461 items, 150 flagged, 5,239 vars | ✅ |
| categorize-items | — | ⏳ Write script next |
| download-items | — | ⏳ |
| upload-items | — | ⏳ |
| import | — | ⏳ |

See `new-migration/product-funnel.md` for full per-stage breakdown and flagging rationale.
