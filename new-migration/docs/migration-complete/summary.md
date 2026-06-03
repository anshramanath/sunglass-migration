# Build & Run — proSPORT Sunglasses Migration

## Prerequisites

- `.env` at repo root with:
  - `BRAND=prosport`
  - `PROSPORT_BASE_URL`, `PROSPORT_CONSUMER_KEY`, `PROSPORT_CONSUMER_SECRET`
  - `SUPABASE_URL`, `SUPABASE_SERVICE_KEY`
  - `DATABASE_URL`
- Schema applied: run `db/001_initial_schema.sql` against Supabase once before first import
- To wipe and re-import: run `db/drop_schema.sql` then `db/001_initial_schema.sql`

All commands run from `new-migration/`.

---

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

---

## QA (run after each stage)

```bash
# Reshape
python qa/verify_reshape_products.py
python qa/verify_reshape_variations.py

# Create items
python qa/verify_create_items.py

# Categorize
python qa/verify_categorize_items.py

# Download
python qa/verify_download_items.py

# Upload
python qa/verify_upload_items.py

# Import
python qa/verify_import.py
```

## Audit (stats and coverage)

```bash
python qa/audit_reshape_products.py
python qa/audit_reshape_variations.py
python qa/audit_create_items.py
python qa/audit_categorize_items.py
python qa/audit_download_items.py
python qa/audit_upload_items.py
python qa/audit_import.py
```

## Analysis

```bash
python analysis/analyze_items.py
```

---

## Completed run — 2026-06-02

| Stage | Result |
|---|---|
| fetch_products | 171 products |
| validate_products | 169 passed, 2 flagged |
| fetch_variations | 1,758 variations |
| validate_variations | 1,740 passed, 18 flagged |
| reshape_products | 169 products |
| reshape_variations | 1,740 variations |
| create_items | 166 passed, 3 flagged |
| prosport_categorize_items | 166 items, 197 leaf assignments |
| download_items | 411 downloaded, 0 failed |
| upload_items | 411 uploaded, 0 failed |
| import_items | 166 products, 1713 variations, 12 categories |

All verify scripts: **PASSED**
