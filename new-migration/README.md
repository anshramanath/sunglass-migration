# Sunglass Monster Migration

Multi-brand WooCommerce → Supabase migration pipeline using the authenticated admin REST API.

## Structure

```
new-migration/
  pipeline/       all pipeline scripts (run in order)
  qa/             verify and audit scripts (run after each stage)
  analysis/       exploratory analysis scripts
  data/           all pipeline output, scoped to data/{slug}/
  db/             schema SQL files
  docs/           per-stage notes, audit results, verify results
```

## Setup

1. Add to `.env` at repo root:
   ```
   BRAND=prosport

   PROSPORT_BASE_URL=https://prosportsunglasses.com
   PROSPORT_CONSUMER_KEY=...
   PROSPORT_CONSUMER_SECRET=...

   SUPABASE_URL=...
   SUPABASE_SERVICE_KEY=...
   DATABASE_URL=...
   ```

2. Apply schema to Supabase (once):
   ```
   db/001_initial_schema.sql
   ```
   To wipe and re-import: run `db/drop_schema.sql` then `db/001_initial_schema.sql`.

All commands run from `new-migration/`.

## Pipeline

### Products
```bash
python pipeline/fetch_products.py
python pipeline/slim_products.py
python pipeline/validate_products.py
```

### Variations
```bash
python pipeline/fetch_variations.py
python pipeline/slim_variations.py
python pipeline/validate_variations.py
```

### Reshape → Create → Categorize
```bash
python pipeline/reshape_products.py
python pipeline/reshape_variations.py
python pipeline/create_items.py
python pipeline/prosport_categorize_items.py
```

### Download → Upload → Import
```bash
python pipeline/download_items.py
python pipeline/upload_items.py
python pipeline/import_items.py
```

## QA

Run after each stage to catch issues before proceeding:

```bash
python qa/verify_reshape_products.py
python qa/verify_reshape_variations.py
python qa/verify_create_items.py
python qa/verify_categorize_items.py
python qa/verify_download_items.py
python qa/verify_upload_items.py
python qa/verify_import.py
```

Audit scripts (stats and coverage):

```bash
python qa/audit_reshape_products.py
python qa/audit_reshape_variations.py
python qa/audit_create_items.py
python qa/audit_categorize_items.py
python qa/audit_download_items.py
python qa/audit_upload_items.py
python qa/audit_import.py
```

## Brands

| Brand | Slug | Status |
|---|---|---|
| proSPORT Sunglasses | `prosport` | ✅ Complete |

## Completed run — proSPORT (2026-06-02)

166 products · 1,713 variations · 12 categories · 411 images

See `docs/migration-complete/summary.md` for full details.

**3 products pending** (2145, 2211, 1208) — fix SKU spaces and missing price in WooCommerce, re-fetch, re-run pipeline.
